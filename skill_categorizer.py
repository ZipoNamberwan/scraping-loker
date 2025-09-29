import pandas as pd
from openai import OpenAI
from datetime import datetime
import json
import time
import os
from collections import Counter
import re

class SkillCategorizer:
    def __init__(self, api_key=None):
        """
        Initialize the skill categorizer with OpenAI API
        """
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            # Try to get from environment variable
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            self.client = OpenAI(api_key=api_key)
        
        self.model = "gpt-5-nano"  # Cheapest available model
        self.delay = 0.5  # Delay between API calls to avoid rate limiting
        
    def categorize_skills(self, skills_list):
        """
        Categorize a list of skills into general categories using ChatGPT
        """
        skills_text = ", ".join(skills_list)
        
        prompt = f"""
Categorize these job skills into general categories. Create broad, meaningful categories that group similar skills together.

Skills to categorize:
{skills_text}

Requirements:
1. Group similar skills into broad categories (e.g., Python, PHP, Java → Programming Languages)
2. Use clear, professional category names
3. Each skill should go to exactly one category
4. Create logical groupings (don't make too many tiny categories)
5. Return ONLY a JSON object mapping each skill to its category
6. Use consistent category names (e.g., "Programming Languages" not "Programming" and "Languages")

Common category examples:
- Programming Languages
- Web Development
- Database Management
- Design & Creative
- Project Management
- Communication & Soft Skills
- Data Analysis & Analytics
- Cloud & Infrastructure
- Mobile Development
- Marketing & Digital Marketing
- Business & Finance
- Quality Assurance & Testing
- DevOps & System Administration
- AI & Machine Learning
- Cybersecurity

JSON format:
{{"skill_name": "Category Name", "another_skill": "Another Category"}}

JSON:
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at categorizing professional skills into logical groups. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            try:
                categorization = json.loads(content)
                if isinstance(categorization, dict):
                    return categorization
                else:
                    print(f"    ⚠️ Unexpected response format: {content[:100]}...")
                    return {}
            except json.JSONDecodeError:
                # Try to extract JSON object from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    try:
                        categorization = json.loads(json_match.group())
                        if isinstance(categorization, dict):
                            return categorization
                    except:
                        pass
                
                print(f"    ⚠️ Could not parse JSON: {content[:100]}...")
                return {}
                
        except Exception as e:
            print(f"    ❌ API Error: {e}")
            return {}
    
    def process_skills_in_batches(self, skills_df, batch_size=20):
        """
        Process skills in batches to avoid token limits and reduce API calls
        """
        all_categorizations = {}
        total_skills = len(skills_df)
        
        print(f"🔄 Processing {total_skills} skills in batches of {batch_size}...")
        
        # Process skills in batches
        for i in range(0, total_skills, batch_size):
            batch = skills_df.iloc[i:i+batch_size]
            batch_skills = batch['skill'].tolist()
            
            batch_num = (i // batch_size) + 1
            total_batches = (total_skills + batch_size - 1) // batch_size
            
            print(f"\n📦 Processing batch {batch_num}/{total_batches} ({len(batch_skills)} skills)")
            print(f"    Skills: {', '.join(batch_skills[:3])}{'...' if len(batch_skills) > 3 else ''}")
            
            # Categorize this batch
            batch_categorization = self.categorize_skills(batch_skills)
            
            if batch_categorization:
                all_categorizations.update(batch_categorization)
                print(f"    ✅ Categorized {len(batch_categorization)} skills")
            else:
                print(f"    ⚠️ Failed to categorize batch")
            
            # Rate limiting
            time.sleep(self.delay)
        
        return all_categorizations
    
    def create_categorized_analysis(self, skills_df, categorizations):
        """
        Create analysis with categorized skills
        """
        # Add categories to original DataFrame
        skills_df_categorized = skills_df.copy()
        skills_df_categorized['category'] = skills_df_categorized['skill'].map(categorizations)
        
        # Handle uncategorized skills
        uncategorized_skills = skills_df_categorized[skills_df_categorized['category'].isna()]
        if not uncategorized_skills.empty:
            print(f"\n⚠️ {len(uncategorized_skills)} skills were not categorized:")
            for skill in uncategorized_skills['skill'].head(10):
                print(f"    - {skill}")
            skills_df_categorized['category'] = skills_df_categorized['category'].fillna('Uncategorized')
        
        # Create category summary
        category_summary = skills_df_categorized.groupby('category').agg({
            'frequency': 'sum',
            'skill': 'count'
        }).reset_index()
        category_summary.columns = ['category', 'total_frequency', 'skill_count']
        category_summary['percentage'] = round((category_summary['total_frequency'] / skills_df_categorized['frequency'].sum()) * 100, 2)
        category_summary = category_summary.sort_values('total_frequency', ascending=False).reset_index(drop=True)
        category_summary['rank'] = category_summary.index + 1
        
        # Reorder columns
        category_summary = category_summary[['rank', 'category', 'skill_count', 'total_frequency', 'percentage']]
        
        # Create detailed skills with categories (sorted by category, then frequency)
        detailed_df = skills_df_categorized.sort_values(['category', 'frequency'], ascending=[True, False]).reset_index(drop=True)
        detailed_df['rank_in_category'] = detailed_df.groupby('category').cumcount() + 1
        
        # Reorder columns for detailed view
        detailed_df = detailed_df[['category', 'rank_in_category', 'skill', 'frequency', 'percentage']]
        
        return category_summary, detailed_df, skills_df_categorized
    
    def save_results(self, category_summary, detailed_df, skills_df_categorized, output_file="skill_extraction_general.xlsx"):
        """
        Save categorized results to Excel file
        """
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Category summary sheet
                category_summary.to_excel(writer, sheet_name='Category Summary', index=False)
                
                # Detailed skills by category sheet
                detailed_df.to_excel(writer, sheet_name='Skills by Category', index=False)
                
                # Original skills with categories
                skills_df_categorized.to_excel(writer, sheet_name='All Skills Categorized', index=False)
                
                # Summary statistics
                total_categories = len(category_summary)
                most_common_category = category_summary.iloc[0] if not category_summary.empty else None
                
                summary_stats = pd.DataFrame({
                    'Metric': [
                        'Total Skill Categories',
                        'Total Unique Skills',
                        'Total Skill Mentions',
                        'Most Common Category',
                        'Most Common Category Skills',
                        'Most Common Category Frequency',
                        'Average Skills per Category'
                    ],
                    'Value': [
                        total_categories,
                        len(skills_df_categorized),
                        skills_df_categorized['frequency'].sum(),
                        most_common_category['category'] if most_common_category is not None else 'N/A',
                        most_common_category['skill_count'] if most_common_category is not None else 0,
                        most_common_category['total_frequency'] if most_common_category is not None else 0,
                        round(len(skills_df_categorized) / total_categories, 1) if total_categories > 0 else 0
                    ]
                })
                
                summary_stats.to_excel(writer, sheet_name='Summary Stats', index=False)
                
                # Format sheets
                workbook = writer.book
                
                # Format Category Summary sheet
                category_worksheet = writer.sheets['Category Summary']
                category_worksheet.column_dimensions['B'].width = 35  # Category name
                category_worksheet.column_dimensions['C'].width = 15  # Skill count
                category_worksheet.column_dimensions['D'].width = 18  # Total frequency
                category_worksheet.column_dimensions['E'].width = 15  # Percentage
                
                # Format Skills by Category sheet
                skills_worksheet = writer.sheets['Skills by Category']
                skills_worksheet.column_dimensions['A'].width = 35  # Category
                skills_worksheet.column_dimensions['C'].width = 40  # Skill name
                
                # Format All Skills Categorized sheet
                all_skills_worksheet = writer.sheets['All Skills Categorized']
                all_skills_worksheet.column_dimensions['E'].width = 35  # Category
                all_skills_worksheet.column_dimensions['B'].width = 40  # Skill name
                
                # Format Summary Stats sheet
                summary_worksheet = writer.sheets['Summary Stats']
                summary_worksheet.column_dimensions['A'].width = 35
                summary_worksheet.column_dimensions['B'].width = 20
            
            print(f"✅ Categorized results saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return False

def main():
    """
    Main function to run skill categorization
    """
    print("=== Skill Categorization with ChatGPT ===")
    print("Converting detailed skills to general categories")
    print("-" * 50)
    
    # Configuration
    input_file = "skill_extraction.xlsx"
    output_file = "skill_extraction_general.xlsx"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        print("Please make sure you have run the skill extraction first.")
        return
    
    # Get API key
    api_key = input("Enter your OpenAI API key (or press Enter if set in environment): ").strip()
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No API key provided. Please set OPENAI_API_KEY environment variable or enter it when prompted.")
            return
    
    try:
        # Read the skills data
        print(f"📖 Reading skills from: {input_file}")
        skills_df = pd.read_excel(input_file, sheet_name='Skills Frequency')
        
        print(f"📊 Found {len(skills_df)} unique skills to categorize")
        
        # Initialize categorizer
        categorizer = SkillCategorizer(api_key)
        
        # Ask for batch size
        print(f"\nProcessing options:")
        print(f"1. Standard processing (20 skills per batch)")
        print(f"2. Fast processing (30 skills per batch)")
        print(f"3. Custom batch size")
        
        choice = input("Choose option (1, 2, or 3): ").strip()
        
        batch_size = 20  # default
        if choice == "2":
            batch_size = 30
        elif choice == "3":
            batch_size = int(input("Enter batch size (10-50): "))
            batch_size = max(10, min(50, batch_size))  # Limit between 10-50
        
        print(f"\n🚀 Starting skill categorization...")
        print(f"   Batch size: {batch_size} skills per API call")
        
        # Process skills in batches
        categorizations = categorizer.process_skills_in_batches(skills_df, batch_size)
        
        if not categorizations:
            print("❌ No skills were categorized!")
            return
        
        print(f"\n📊 CATEGORIZATION COMPLETE:")
        print(f"   Skills categorized: {len(categorizations)}")
        print(f"   Skills not categorized: {len(skills_df) - len(categorizations)}")
        
        # Create analysis
        category_summary, detailed_df, skills_df_categorized = categorizer.create_categorized_analysis(skills_df, categorizations)
        
        # Show top categories
        print(f"\n🏆 Top 10 skill categories:")
        for _, row in category_summary.head(10).iterrows():
            print(f"   {row['rank']}. {row['category']} - {row['skill_count']} skills ({row['percentage']}%)")
        
        # Save results
        if categorizer.save_results(category_summary, detailed_df, skills_df_categorized, output_file):
            print(f"\n✅ SUCCESS!")
            print(f"   Results saved to: {output_file}")
            print(f"   - Category Summary: {len(category_summary)} categories")
            print(f"   - Skills by Category: {len(detailed_df)} skills organized by category")
            print(f"   - All Skills Categorized: Complete list with categories")
            print(f"   - Summary Stats: Overall statistics")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()