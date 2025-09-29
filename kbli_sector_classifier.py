import pandas as pd
from openai import OpenAI
from datetime import datetime
import json
import time
import os
from collections import Counter
import re

class KBLISectorClassifier:
    def __init__(self, api_key=None):
        """
        Initialize the KBLI sector classifier with OpenAI API
        """
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            # Try to get from environment variable
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            self.client = OpenAI(api_key=api_key)
        
        self.model = "gpt-4o-mini"  # Using the cheapest available model
        self.delay = 1  # Delay between API calls to avoid rate limiting
        
        # KBLI Sectors reference (Indonesian version)
        self.kbli_sectors = {
            'A': 'Pertanian, Kehutanan dan Perikanan',
            'B': 'Pertambangan dan Penggalian', 
            'C': 'Industri Pengolahan',
            'D': 'Pengadaan Listrik, Gas, Uap dan Udara Dingin',
            'E': 'Pengelolaan Air, Pengelolaan Air Limbah, Pengelolaan dan Daur Ulang Sampah, dan Aktivitas Remediasi',
            'F': 'Konstruksi',
            'G': 'Perdagangan Besar dan Eceran; Reparasi dan Perawatan Mobil dan Sepeda Motor',
            'H': 'Transportasi dan Pergudangan',
            'I': 'Penyediaan Akomodasi dan Penyediaan Makan Minum',
            'J': 'Informasi dan Komunikasi',
            'K': 'Aktivitas Keuangan dan Asuransi',
            'L': 'Real Estat',
            'M': 'Aktivitas Profesional, Ilmiah dan Teknis',
            'N': 'Aktivitas Penyewaan dan Sewa Guna Usaha Tanpa Hak Opsi, Ketenagakerjaan, Agen Perjalanan dan Penunjang Usaha Lainnya',
            'O': 'Administrasi Pemerintahan, Pertahanan dan Jaminan Sosial Wajib',
            'P': 'Pendidikan',
            'Q': 'Aktivitas Kesehatan Manusia dan Aktivitas Sosial',
            'R': 'Kesenian, Hiburan dan Rekreasi',
            'S': 'Aktivitas Jasa Lainnya',
            'T': 'Aktivitas Rumah Tangga Sebagai Pemberi Kerja; Aktivitas Yang Menghasilkan Barang dan Jasa Oleh Rumah Tangga Yang Digunakan Sendiri Untuk Memenuhi Kebutuhan',
            'U': 'Aktivitas Badan Internasional dan Badan Ekstra Internasional Lainnya'
        }
    
    def classify_job_sectors(self, jobs_list):
        """
        Classify jobs into KBLI sectors using ChatGPT
        """
        jobs_text = "\n".join([f"{i+1}. {job}" for i, job in enumerate(jobs_list)])
        
        sectors_description = "\n".join([f"{code}: {desc}" for code, desc in self.kbli_sectors.items()])
        
        prompt = f"""
Klasifikasikan lowongan kerja ini ke dalam sektor KBLI (Klasifikasi Baku Lapangan Usaha Indonesia). 
Gunakan HANYA huruf sektor (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U).

Sektor KBLI:
{sectors_description}

Lowongan Kerja yang akan Diklasifikasi:
{jobs_text}

Persyaratan:
1. Analisis judul pekerjaan, jenis perusahaan, deskripsi pekerjaan, dan keahlian yang dibutuhkan
2. Tentukan sektor KBLI yang paling sesuai (A-U)
3. Pertimbangkan aktivitas bisnis UTAMA dari pemberi kerja
4. Jika tidak jelas, pilih sektor yang paling mungkin berdasarkan informasi yang tersedia
5. Berikan HANYA array JSON dengan huruf sektor sesuai urutan pekerjaan
6. Setiap pekerjaan mendapat tepat satu huruf sektor
7. Konten bisa dalam bahasa Indonesia atau Inggris, tapi klasifikasi berdasarkan sektor KBLI Indonesia

Contoh format: ["J", "C", "G", "M", "I"]

Array JSON:
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Anda adalah ahli dalam klasifikasi bisnis Indonesia (KBLI) dan analisis pasar kerja. Selalu berikan respons dengan array JSON huruf sektor yang valid saja. Konten pekerjaan bisa dalam bahasa Indonesia atau Inggris."},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            try:
                sectors = json.loads(content)
                if isinstance(sectors, list) and len(sectors) == len(jobs_list):
                    # Validate sector codes
                    validated_sectors = []
                    for sector in sectors:
                        if isinstance(sector, str) and sector.upper() in self.kbli_sectors:
                            validated_sectors.append(sector.upper())
                        else:
                            validated_sectors.append('Unknown')
                    return validated_sectors
                else:
                    print(f"    ⚠️ Incorrect response length: expected {len(jobs_list)}, got {len(sectors) if isinstance(sectors, list) else 'non-list'}")
                    return ['Unknown'] * len(jobs_list)
            except json.JSONDecodeError:
                # Try to extract JSON array from response
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    try:
                        sectors = json.loads(json_match.group())
                        if isinstance(sectors, list) and len(sectors) == len(jobs_list):
                            validated_sectors = []
                            for sector in sectors:
                                if isinstance(sector, str) and sector.upper() in self.kbli_sectors:
                                    validated_sectors.append(sector.upper())
                                else:
                                    validated_sectors.append('Unknown')
                            return validated_sectors
                    except:
                        pass
                
                print(f"    ⚠️ Could not parse JSON: {content[:100]}...")
                return ['Unknown'] * len(jobs_list)
                
        except Exception as e:
            print(f"    ❌ API Error: {e}")
            return ['Unknown'] * len(jobs_list)
    
    def process_file(self, file_path, columns_to_use, batch_size=10):
        """
        Process a single Excel file and classify jobs
        """
        print(f"\n📁 Processing: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"  ❌ File not found: {file_path}")
            return None
        
        try:
            df = pd.read_excel(file_path)
            print(f"  📊 Loaded {len(df)} jobs")
            
            # Check if columns exist
            existing_columns = [col for col in columns_to_use if col in df.columns]
            missing_columns = [col for col in columns_to_use if col not in df.columns]
            
            if missing_columns:
                print(f"  ⚠️ Missing columns: {missing_columns}")
            if not existing_columns:
                print(f"  ❌ No specified columns found in file")
                return None
            
            print(f"  ✅ Using columns: {existing_columns}")
            
            # Combine columns to create job descriptions
            job_descriptions = []
            for index, row in df.iterrows():
                parts = []
                for col in existing_columns:
                    value = row[col]
                    if pd.notna(value) and str(value).strip():
                        parts.append(f"{col}: {str(value).strip()}")
                
                if parts:
                    job_descriptions.append(" | ".join(parts))
                else:
                    job_descriptions.append("No information available")
            
            # Process in batches
            all_sectors = []
            total_jobs = len(job_descriptions)
            
            print(f"  🔄 Processing {total_jobs} jobs in batches of {batch_size}...")
            
            for i in range(0, total_jobs, batch_size):
                batch = job_descriptions[i:i+batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = (total_jobs + batch_size - 1) // batch_size
                
                print(f"    📦 Batch {batch_num}/{total_batches} ({len(batch)} jobs)")
                
                # Classify this batch
                batch_sectors = self.classify_job_sectors(batch)
                all_sectors.extend(batch_sectors)
                
                # Rate limiting
                time.sleep(self.delay)
            
            # Add results to DataFrame
            df['kbli_sector'] = all_sectors
            df['sector_description'] = df['kbli_sector'].map(self.kbli_sectors).fillna('Sektor Tidak Dikenal')
            df['job_combined_info'] = job_descriptions
            df['source_file'] = os.path.basename(file_path)
            
            print(f"  ✅ Classification complete")
            return df
            
        except Exception as e:
            print(f"  ❌ Error processing file: {e}")
            return None
    
    def process_all_files(self):
        """
        Process all three job files
        """
        # Define files and their columns
        files_config = [
            ("glints_jobs_full_20250928_074044.xlsx", ["job_title", "required_skills", "job_description"]),
            ("jobstreet_jobs_20250926_053327.xlsx", ["title", "teaser", "classification", "subclassification", "job_content"]),
            ("loker_jobs_20250924_221954.xlsx", ["title", "category", "content", "job_description"])
        ]
        
        all_dataframes = []
        
        for file_path, columns in files_config:
            df = self.process_file(file_path, columns, batch_size=10)
            if df is not None:
                all_dataframes.append(df)
        
        if not all_dataframes:
            print("❌ No files were processed successfully")
            return None
        
        # Combine all dataframes
        print(f"\n🔗 Combining results from {len(all_dataframes)} files...")
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        
        return combined_df
    
    def create_sector_analysis(self, df):
        """
        Create analysis of sector classification results
        """
        # Sector summary
        sector_summary = df['kbli_sector'].value_counts().reset_index()
        sector_summary.columns = ['sector_code', 'job_count']
        sector_summary['sector_description'] = sector_summary['sector_code'].map(self.kbli_sectors).fillna('Sektor Tidak Dikenal')
        sector_summary['percentage'] = round((sector_summary['job_count'] / len(df)) * 100, 2)
        sector_summary = sector_summary.sort_values('job_count', ascending=False).reset_index(drop=True)
        sector_summary['rank'] = sector_summary.index + 1
        
        # Reorder columns
        sector_summary = sector_summary[['rank', 'sector_code', 'sector_description', 'job_count', 'percentage']]
        
        # File source summary
        source_summary = df.groupby(['source_file', 'kbli_sector']).size().reset_index(name='count')
        source_pivot = source_summary.pivot(index='source_file', columns='kbli_sector', values='count').fillna(0)
        
        # Summary statistics
        summary_stats = pd.DataFrame({
            'Metric': [
                'Total Jobs Classified',
                'Number of Different Sectors',
                'Most Common Sector',
                'Most Common Sector Count',
                'Jobs from Glints',
                'Jobs from JobStreet',
                'Jobs from Loker',
                'Unknown Classifications'
            ],
            'Value': [
                len(df),
                len(sector_summary[sector_summary['sector_code'] != 'Unknown']),
                sector_summary.iloc[0]['sector_code'] + ' - ' + sector_summary.iloc[0]['sector_description'] if not sector_summary.empty else 'N/A',
                sector_summary.iloc[0]['job_count'] if not sector_summary.empty else 0,
                len(df[df['source_file'].str.contains('glints', case=False, na=False)]),
                len(df[df['source_file'].str.contains('jobstreet', case=False, na=False)]),
                len(df[df['source_file'].str.contains('loker', case=False, na=False)]),
                len(df[df['kbli_sector'] == 'Unknown'])
            ]
        })
        
        return sector_summary, source_pivot, summary_stats
    
    def save_results(self, df, sector_summary, source_pivot, summary_stats, output_file="sector_classification.xlsx"):
        """
        Save classification results to Excel file
        """
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Main results - all jobs with classifications
                df.to_excel(writer, sheet_name='Job Classifications', index=False)
                
                # Sector summary
                sector_summary.to_excel(writer, sheet_name='Sector Summary', index=False)
                
                # Source file breakdown
                source_pivot.to_excel(writer, sheet_name='Source Breakdown')
                
                # Summary statistics
                summary_stats.to_excel(writer, sheet_name='Summary Stats', index=False)
                
                # Format sheets
                workbook = writer.book
                
                # Format Job Classifications sheet
                jobs_worksheet = writer.sheets['Job Classifications']
                # Auto-adjust some key columns
                jobs_worksheet.column_dimensions['A'].width = 15  # sector
                jobs_worksheet.column_dimensions['B'].width = 40  # sector description
                
                # Format Sector Summary sheet
                sector_worksheet = writer.sheets['Sector Summary']
                sector_worksheet.column_dimensions['C'].width = 50  # sector description
                
                # Format Summary Stats sheet
                summary_worksheet = writer.sheets['Summary Stats']
                summary_worksheet.column_dimensions['A'].width = 30
                summary_worksheet.column_dimensions['B'].width = 25
            
            print(f"✅ Classification results saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return False

def main():
    """
    Main function to run KBLI sector classification
    """
    print("=== KBLI Sector Classification ===")
    print("Classifying Indonesian job postings into KBLI sectors")
    print("-" * 50)
    
    # Get API key
    api_key = input("Enter your OpenAI API key (or press Enter if set in environment): ").strip()
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No API key provided. Please set OPENAI_API_KEY environment variable or enter it when prompted.")
            return
    
    try:
        # Initialize classifier
        classifier = KBLISectorClassifier(api_key)
        
        print("\n🇮🇩 KBLI Sectors Reference:")
        for code, desc in list(classifier.kbli_sectors.items())[:10]:  # Show first 10
            print(f"   {code}: {desc}")
        print(f"   ... and {len(classifier.kbli_sectors)-10} more sectors")
        
        print(f"\n🚀 Starting KBLI classification...")
        
        # Process all files
        combined_df = classifier.process_all_files()
        
        if combined_df is None:
            return
        
        print(f"\n📊 CLASSIFICATION COMPLETE:")
        print(f"   Total jobs classified: {len(combined_df)}")
        
        # Create analysis
        sector_summary, source_pivot, summary_stats = classifier.create_sector_analysis(combined_df)
        
        # Show top sectors
        print(f"\n🏆 Top 10 job sectors:")
        for _, row in sector_summary.head(10).iterrows():
            print(f"   {row['rank']}. {row['sector_code']} - {row['sector_description']}: {row['job_count']} jobs ({row['percentage']}%)")
        
        # Save results
        if classifier.save_results(combined_df, sector_summary, source_pivot, summary_stats):
            print(f"\n✅ SUCCESS!")
            print(f"   Results saved to: sector_classification.xlsx")
            print(f"   - Job Classifications: {len(combined_df)} jobs with KBLI sectors")
            print(f"   - Sector Summary: {len(sector_summary)} different sectors found")
            print(f"   - Source Breakdown: Classification by file source")
            print(f"   - Summary Stats: Overall statistics")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()