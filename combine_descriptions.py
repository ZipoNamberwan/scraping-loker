import pandas as pd
from datetime import datetime
import os

def combine_descriptions_from_files():
    """
    Combine text descriptions from multiple Excel files into a single file
    """
    
    # Define the files and their text columns in desired order
    # Order: 1. loker_jobs, 2. jobstreet, 3. glints
    files_config = [
        ("loker_jobs_20250924_221954.xlsx", ["content", "job_description", "responsibilities", "qualifications"]),
        ("jobstreet_jobs_20250926_053327.xlsx", ["job_description"]),
        ("glints_jobs_full_20250928_074044.xlsx", ["required_skills"])
    ]
    
    all_descriptions = []
    
    print("=== Combining Descriptions from Multiple Files ===")
    print("Processing order: 1. Loker Jobs → 2. JobStreet → 3. Glints")
    print("-" * 50)
    
    for file_path, columns in files_config:
        print(f"\nProcessing: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"  ❌ File not found: {file_path}")
            continue
        
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            print(f"  📊 Loaded {len(df)} rows")
            
            # Check which columns exist
            existing_columns = [col for col in columns if col in df.columns]
            missing_columns = [col for col in columns if col not in df.columns]
            
            if missing_columns:
                print(f"  ⚠️  Missing columns: {missing_columns}")
            if existing_columns:
                print(f"  ✅ Found columns: {existing_columns}")
            
            # Extract descriptions from existing columns
            file_descriptions = []
            
            # Special handling for loker_jobs file - combine multiple columns into one description
            if "loker_jobs" in file_path.lower():
                print(f"  📋 Combining columns for loker_jobs file...")
                
                # Process each row and combine all available columns
                for index, row in df.iterrows():
                    combined_parts = []
                    
                    # Check each column and add if it has content
                    for col in existing_columns:
                        value = row[col]
                        if pd.notna(value) and str(value).strip() != '' and str(value).strip().lower() != 'nan':
                            # Format the column with a label
                            label = col.replace('_', ' ').title()  # Convert job_description to Job Description
                            combined_parts.append(f"{label}: {str(value).strip()}")
                    
                    # Only add if we have at least one part
                    if combined_parts:
                        combined_description = "\n\n".join(combined_parts)
                        file_descriptions.append({
                            'description': combined_description,
                            'source_file': file_path,
                            'source_column': 'combined_columns',
                            'original_row_index': index
                        })
                
                print(f"    - Combined columns: {len(file_descriptions)} combined descriptions")
            
            else:
                # Regular processing for other files - each column separately
                for col in existing_columns:
                    column_data = df[col].dropna()  # Remove NaN values
                    
                    # Convert to string and filter out empty strings
                    valid_descriptions = []
                    for desc in column_data:
                        if pd.notna(desc) and str(desc).strip() != '' and str(desc).strip().lower() != 'nan':
                            valid_descriptions.append(str(desc).strip())
                    
                    print(f"    - {col}: {len(valid_descriptions)} valid descriptions")
                    
                    # Add to file descriptions with source info
                    for desc in valid_descriptions:
                        file_descriptions.append({
                            'description': desc,
                            'source_file': file_path,
                            'source_column': col,
                            'original_row_index': None  # We could add this if needed
                        })
            
            all_descriptions.extend(file_descriptions)
            print(f"  📝 Total descriptions from this file: {len(file_descriptions)}")
            
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
            continue
    
    print(f"\n" + "=" * 50)
    print(f"📋 SUMMARY:")
    print(f"   Total descriptions collected: {len(all_descriptions)}")
    
    if not all_descriptions:
        print("❌ No descriptions found to combine!")
        return
    
    # Create DataFrame
    combined_df = pd.DataFrame(all_descriptions)
    
    # Show statistics by source
    print(f"\n📊 Descriptions by source:")
    source_stats = combined_df.groupby(['source_file', 'source_column']).size().reset_index(name='count')
    for _, row in source_stats.iterrows():
        filename = os.path.basename(row['source_file'])
        print(f"   {filename} - {row['source_column']}: {row['count']}")
    
    # Remove duplicates (optional)
    original_count = len(combined_df)
    combined_df_unique = combined_df.drop_duplicates(subset=['description'])
    duplicate_count = original_count - len(combined_df_unique)
    
    print(f"\n🔄 Duplicate removal:")
    print(f"   Original descriptions: {original_count}")
    print(f"   Unique descriptions: {len(combined_df_unique)}")
    print(f"   Duplicates removed: {duplicate_count}")
    
    # Create final output with just the description column
    final_df = pd.DataFrame({
        'description': combined_df_unique['description'].values
    })
    
    # Also create a detailed version with source information
    detailed_df = combined_df_unique.copy()
    
    # Save to Excel
    output_filename = "combined_description.xlsx"
    
    try:
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
            # Main sheet with just descriptions
            final_df.to_excel(writer, sheet_name='Descriptions', index=False)
            
            # Detailed sheet with source information
            detailed_df.to_excel(writer, sheet_name='Detailed', index=False)
            
            # Summary statistics
            summary_df = pd.DataFrame({
                'Metric': [
                    'Total Files Processed',
                    'Total Descriptions (with duplicates)',
                    'Unique Descriptions',
                    'Duplicates Removed',
                    'JobStreet Descriptions',
                    'Glints Descriptions', 
                    'Loker Descriptions'
                ],
                'Value': [
                    len([f for f, c in files_config if os.path.exists(f)]),
                    original_count,
                    len(combined_df_unique),
                    duplicate_count,
                    len(combined_df_unique[combined_df_unique['source_file'].str.contains('jobstreet', case=False, na=False)]),
                    len(combined_df_unique[combined_df_unique['source_file'].str.contains('glints', case=False, na=False)]),
                    len(combined_df_unique[combined_df_unique['source_file'].str.contains('loker', case=False, na=False)])
                ]
            })
            
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Format worksheets
            workbook = writer.book
            
            # Format main descriptions sheet
            desc_worksheet = writer.sheets['Descriptions']
            desc_worksheet.column_dimensions['A'].width = 100  # Wide column for descriptions
            
            # Format detailed sheet
            detailed_worksheet = writer.sheets['Detailed']
            detailed_worksheet.column_dimensions['A'].width = 80  # Description column
            detailed_worksheet.column_dimensions['B'].width = 30  # Source file column
            detailed_worksheet.column_dimensions['C'].width = 20  # Source column
            
            # Format summary sheet
            summary_worksheet = writer.sheets['Summary']
            summary_worksheet.column_dimensions['A'].width = 30
            summary_worksheet.column_dimensions['B'].width = 15
        
        print(f"\n✅ Combined descriptions saved to: {output_filename}")
        print(f"   - Sheet 1: 'Descriptions' - {len(final_df)} descriptions only")
        print(f"   - Sheet 2: 'Detailed' - with source file and column information")
        print(f"   - Sheet 3: 'Summary' - processing statistics")
        
        # Show first few descriptions as sample
        print(f"\n📝 Sample descriptions (first 3):")
        for i, desc in enumerate(final_df['description'].head(3)):
            preview = desc[:100] + "..." if len(desc) > 100 else desc
            print(f"   {i+1}. {preview}")
        
        return final_df
        
    except Exception as e:
        print(f"❌ Error saving to Excel: {e}")
        return None

def main():
    """Main function to run the description combination"""
    print("=== Description Combiner ===")
    print("Combining descriptions from multiple job files...")
    print("-" * 40)
    
    # Combine descriptions
    result = combine_descriptions_from_files()
    
    if result is not None:
        print("\n" + "=" * 40)
        print("✅ Process completed successfully!")
        print(f"Combined {len(result)} unique descriptions into 'combined_description.xlsx'")
    else:
        print("\n" + "=" * 40)
        print("❌ Process failed!")

if __name__ == "__main__":
    main()