import pandas as pd
from datetime import datetime
import os

def extract_skills_to_dictionary(excel_file_path):
    """
    Extract skills from the required_skills column and create a skill dictionary
    where each skill is on its own row with a count of how many times it appears.
    """
    
    # Check if file exists
    if not os.path.exists(excel_file_path):
        print(f"Error: File {excel_file_path} not found!")
        return
    
    try:
        # Read the Excel file
        print(f"Reading Excel file: {excel_file_path}")
        df = pd.read_excel(excel_file_path)
        
        # Check if required_skills column exists
        if 'required_skills' not in df.columns:
            print("Error: 'required_skills' column not found in the Excel file!")
            print(f"Available columns: {list(df.columns)}")
            return
        
        print(f"Found {len(df)} rows in the dataset")
        
        # Extract all skills
        all_skills = []
        rows_with_skills = 0
        
        for index, row in df.iterrows():
            skills_value = row['required_skills']
            
            # Skip if the cell is empty or NaN
            if pd.isna(skills_value) or skills_value == '':
                continue
            
            rows_with_skills += 1
            
            # Split skills by ' | ' and clean them
            if isinstance(skills_value, str):
                skills = [skill.strip() for skill in skills_value.split(' | ')]
                # Remove empty skills
                skills = [skill for skill in skills if skill and skill != '']
                all_skills.extend(skills)
        
        print(f"Found {rows_with_skills} rows with skills data")
        print(f"Total skills extracted: {len(all_skills)}")
        
        # Create skill dictionary with counts
        skill_counts = {}
        for skill in all_skills:
            if skill in skill_counts:
                skill_counts[skill] += 1
            else:
                skill_counts[skill] = 1
        
        # Convert to DataFrame
        skill_df = pd.DataFrame([
            {'skill': skill, 'count': count, 'percentage': round((count / len(all_skills)) * 100, 2)}
            for skill, count in skill_counts.items()
        ])
        
        # Sort by count (descending)
        skill_df = skill_df.sort_values('count', ascending=False).reset_index(drop=True)
        
        # Add rank
        skill_df['rank'] = skill_df.index + 1
        
        # Reorder columns
        skill_df = skill_df[['rank', 'skill', 'count', 'percentage']]
        
        print(f"Unique skills found: {len(skill_df)}")
        print(f"\nTop 10 most common skills:")
        print(skill_df.head(10).to_string(index=False))
        
        # Save to Excel
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = "skill_dictionary.xlsx"
        
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
            # Main skill dictionary
            skill_df.to_excel(writer, sheet_name='Skill Dictionary', index=False)
            
            # Summary statistics
            summary_df = pd.DataFrame({
                'Metric': [
                    'Total Job Postings',
                    'Job Postings with Skills',
                    'Total Skill Mentions',
                    'Unique Skills',
                    'Average Skills per Job',
                    'Most Common Skill',
                    'Most Common Skill Count'
                ],
                'Value': [
                    len(df),
                    rows_with_skills,
                    len(all_skills),
                    len(skill_df),
                    round(len(all_skills) / rows_with_skills, 2) if rows_with_skills > 0 else 0,
                    skill_df.iloc[0]['skill'] if not skill_df.empty else 'N/A',
                    skill_df.iloc[0]['count'] if not skill_df.empty else 0
                ]
            })
            
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Get the workbook and worksheets for formatting
            workbook = writer.book
            
            # Format Skill Dictionary sheet
            skill_worksheet = writer.sheets['Skill Dictionary']
            
            # Auto-adjust column widths for skill dictionary
            for column in skill_worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # Max width of 50
                skill_worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Format Summary sheet
            summary_worksheet = writer.sheets['Summary']
            
            # Auto-adjust column widths for summary
            for column in summary_worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 30)  # Max width of 30
                summary_worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"\n✅ Skill dictionary saved to: {output_filename}")
        print(f"   - Sheet 1: 'Skill Dictionary' with {len(skill_df)} unique skills")
        print(f"   - Sheet 2: 'Summary' with overall statistics")
        
        return skill_df
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def main():
    """Main function to run the skill extraction"""
    # File path
    excel_file = "glints_jobs_full_20250928_074044.xlsx"
    
    print("=== Skill Dictionary Extractor ===")
    print(f"Processing: {excel_file}")
    print("-" * 40)
    
    # Extract skills
    result = extract_skills_to_dictionary(excel_file)
    
    if result is not None:
        print("\n" + "=" * 40)
        print("✅ Process completed successfully!")
    else:
        print("\n" + "=" * 40)
        print("❌ Process failed!")

if __name__ == "__main__":
    main()
