import pandas as pd
from openai import OpenAI
from datetime import datetime
import json
import time
import os
from collections import Counter
import re

class SkillExtractor:
    def __init__(self, api_key=None):
        """
        Initialize the skill extractor with OpenAI API
        """
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            # Try to get from environment variable
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            self.client = OpenAI(api_key=api_key)
        
        self.model = "gpt-4o-mini"  # Cheapest available model
        self.delay = 1  # Delay between API calls to avoid rate limiting
        
    def extract_skills_from_text(self, description):
        """
        Extract skills from a job description using ChatGPT
        """
        prompt = f"""
Extract all technical skills, tools, programming languages, frameworks, and professional skills mentioned in this job description. 

Job Description:
{description}

Requirements:
1. Extract ALL skills mentioned (technical, soft skills, tools, languages, frameworks, etc.)
2. If the text is in Indonesian, translate the skills to English
3. Standardize skill names (e.g., "Javascript" → "JavaScript", "Reactjs" → "React")
4. Return ONLY a JSON array of skills, no other text
5. Each skill should be a single string in the array
6. Remove duplicates and similar variations

Example output format:
["Python", "JavaScript", "React", "SQL", "Communication", "Problem Solving"]

JSON Array:
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert job skill extractor. Extract and standardize all skills from job descriptions. Always respond with only a valid JSON array."},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=500
                # Note: temperature parameter removed as it's not supported by all models
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            try:
                skills = json.loads(content)
                if isinstance(skills, list):
                    # Clean and validate skills
                    cleaned_skills = []
                    for skill in skills:
                        if isinstance(skill, str) and skill.strip():
                            cleaned_skills.append(skill.strip())
                    return cleaned_skills
                else:
                    print(f"    ⚠️ Unexpected response format: {content[:100]}...")
                    return []
            except json.JSONDecodeError:
                # Try to extract JSON array from response
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    try:
                        skills = json.loads(json_match.group())
                        if isinstance(skills, list):
                            cleaned_skills = []
                            for skill in skills:
                                if isinstance(skill, str) and skill.strip():
                                    cleaned_skills.append(skill.strip())
                            return cleaned_skills
                    except:
                        pass
                
                print(f"    ⚠️ Could not parse JSON: {content[:100]}...")
                return []
                
        except Exception as e:
            print(f"    ❌ API Error: {e}")
            return []
    
    def process_descriptions(self, excel_file, max_descriptions=None, start_from=0):
        """
        Process job descriptions and extract skills
        """
        # Read the combined descriptions file
        if not os.path.exists(excel_file):
            print(f"❌ File not found: {excel_file}")
            return None
        
        print(f"📖 Reading descriptions from: {excel_file}")
        df = pd.read_excel(excel_file, sheet_name='Descriptions')
        
        total_descriptions = len(df)
        print(f"📊 Total descriptions: {total_descriptions}")
        
        # Apply limits if specified
        if start_from > 0:
            df = df.iloc[start_from:]
            print(f"⏭️ Starting from index {start_from}")
        
        if max_descriptions:
            df = df.head(max_descriptions)
            print(f"🔢 Processing max {max_descriptions} descriptions")
        
        print(f"🎯 Processing {len(df)} descriptions...")
        
        # Store results
        all_skills = []
        processed_results = []
        
        for index, row in df.iterrows():
            description = row['description']
            actual_index = start_from + index if start_from > 0 else index
            
            print(f"\n📝 Processing description {actual_index + 1}/{total_descriptions}")
            print(f"    Preview: {description[:100]}...")
            
            # Extract skills
            skills = self.extract_skills_from_text(description)
            
            if skills:
                print(f"    ✅ Extracted {len(skills)} skills: {', '.join(skills[:5])}{'...' if len(skills) > 5 else ''}")
                all_skills.extend(skills)
                
                # Store individual result
                processed_results.append({
                    'original_index': actual_index,
                    'description_preview': description[:200] + "..." if len(description) > 200 else description,
                    'extracted_skills': ', '.join(skills),
                    'skill_count': len(skills)
                })
            else:
                print(f"    ⚠️ No skills extracted")
                processed_results.append({
                    'original_index': actual_index,
                    'description_preview': description[:200] + "..." if len(description) > 200 else description,
                    'extracted_skills': '',
                    'skill_count': 0
                })
            
            # Rate limiting
            time.sleep(self.delay)
        
        return all_skills, processed_results
    
    def create_skill_frequency_analysis(self, all_skills, processed_results):
        """
        Create frequency analysis of extracted skills
        """
        # Count skill frequencies
        skill_counter = Counter(all_skills)
        
        # Create skills DataFrame
        skills_df = pd.DataFrame([
            {
                'rank': i + 1,
                'skill': skill,
                'frequency': count,
                'percentage': round((count / len(all_skills)) * 100, 2) if all_skills else 0
            }
            for i, (skill, count) in enumerate(skill_counter.most_common())
        ])
        
        # Create processing results DataFrame
        results_df = pd.DataFrame(processed_results)
        
        # Create summary statistics
        summary_df = pd.DataFrame({
            'Metric': [
                'Total Descriptions Processed',
                'Total Skills Extracted',
                'Unique Skills',
                'Average Skills per Description',
                'Descriptions with Skills',
                'Descriptions without Skills',
                'Most Common Skill',
                'Most Common Skill Frequency'
            ],
            'Value': [
                len(processed_results),
                len(all_skills),
                len(skills_df),
                round(len(all_skills) / len(processed_results), 2) if processed_results else 0,
                len([r for r in processed_results if r['skill_count'] > 0]),
                len([r for r in processed_results if r['skill_count'] == 0]),
                skills_df.iloc[0]['skill'] if not skills_df.empty else 'N/A',
                skills_df.iloc[0]['frequency'] if not skills_df.empty else 0
            ]
        })
        
        return skills_df, results_df, summary_df
    
    def save_results(self, skills_df, results_df, summary_df, output_file="skill_extraction.xlsx"):
        """
        Save results to Excel file
        """
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Skills frequency sheet
                skills_df.to_excel(writer, sheet_name='Skills Frequency', index=False)
                
                # Processing results sheet
                results_df.to_excel(writer, sheet_name='Processing Results', index=False)
                
                # Summary sheet
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Format sheets
                workbook = writer.book
                
                # Format Skills Frequency sheet
                skills_worksheet = writer.sheets['Skills Frequency']
                skills_worksheet.column_dimensions['B'].width = 40  # Skill name
                skills_worksheet.column_dimensions['C'].width = 15  # Frequency
                skills_worksheet.column_dimensions['D'].width = 15  # Percentage
                
                # Format Processing Results sheet
                results_worksheet = writer.sheets['Processing Results']
                results_worksheet.column_dimensions['B'].width = 80  # Description preview
                results_worksheet.column_dimensions['C'].width = 60  # Extracted skills
                
                # Format Summary sheet
                summary_worksheet = writer.sheets['Summary']
                summary_worksheet.column_dimensions['A'].width = 30
                summary_worksheet.column_dimensions['B'].width = 20
            
            print(f"✅ Results saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return False

def main():
    """
    Main function to run skill extraction
    """
    print("=== Job Skill Extractor with ChatGPT ===")
    print("Using gpt-3.5-turbo (cheapest model)")
    print("-" * 50)
    
    # Configuration
    input_file = "combined_description.xlsx"
    output_file = "skill_extraction.xlsx"
    
    # Get API key
    api_key = input("Enter your OpenAI API key (or press Enter if set in environment): ").strip()
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No API key provided. Please set OPENAI_API_KEY environment variable or enter it when prompted.")
            return
    
    try:
        # Initialize extractor
        extractor = SkillExtractor(api_key)
        
        # Ask for processing limits
        print(f"\nProcessing options:")
        print(f"1. Process all descriptions (might be expensive)")
        print(f"2. Process limited number for testing")
        
        choice = input("Choose option (1 or 2): ").strip()
        
        max_descriptions = None
        start_from = 0
        
        if choice == "2":
            max_descriptions = int(input("How many descriptions to process? "))
            start_from_input = input("Start from index (0 for beginning): ").strip()
            if start_from_input:
                start_from = int(start_from_input)
        
        print(f"\n🚀 Starting skill extraction...")
        
        # Process descriptions
        result = extractor.process_descriptions(input_file, max_descriptions, start_from)
        
        if result is None:
            return
        
        all_skills, processed_results = result
        
        print(f"\n📊 EXTRACTION COMPLETE:")
        print(f"   Total skills extracted: {len(all_skills)}")
        print(f"   Unique skills: {len(set(all_skills))}")
        
        # Create analysis
        skills_df, results_df, summary_df = extractor.create_skill_frequency_analysis(all_skills, processed_results)
        
        # Show top skills
        print(f"\n🏆 Top 10 most frequent skills:")
        for _, row in skills_df.head(10).iterrows():
            print(f"   {row['rank']}. {row['skill']} - {row['frequency']} times ({row['percentage']}%)")
        
        # Save results
        if extractor.save_results(skills_df, results_df, summary_df, output_file):
            print(f"\n✅ SUCCESS!")
            print(f"   Results saved to: {output_file}")
            print(f"   - Skills Frequency: {len(skills_df)} unique skills")
            print(f"   - Processing Results: {len(results_df)} descriptions processed")
            print(f"   - Summary: Overall statistics")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()