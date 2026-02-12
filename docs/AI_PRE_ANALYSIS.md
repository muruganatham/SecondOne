# AI Query System - Pre-Analysis Enhancement

## Problem Statement
The AI was frequently generating SQL queries for tables that don't exist in the database, resulting in errors like:
- "Table 'srec_2025_2_test_data' doesn't exist"
- Generic error messages that don't help users understand what went wrong

## Solution: Two-Step AI Process

### Step 1: Pre-Analysis (NEW)
Before generating any SQL, the AI now:
1. **Analyzes the question** to understand what data is needed
2. **Identifies required tables** based on the question
3. **Validates table existence** against the actual database
4. **Determines query type** (simple/complex/general knowledge)
5. **Provides confidence level** for the analysis

### Step 2: SQL Generation (Enhanced)
Only proceeds if:
- All required tables exist in the database, OR
- The question is general knowledge (doesn't need database access)

## Technical Implementation

### New Method: `analyze_question_and_tables()`
**Location**: `backend/app/services/ai_service.py`

**Purpose**: Pre-validates that the AI can answer the question with available data

**Returns**:
```python
{
    "tables_needed": ["users", "assessments"],
    "tables_available": ["users"],
    "tables_missing": ["assessments"],
    "can_proceed": False,
    "query_type": "complex",
    "reasoning": "Need to join users with assessment data",
    "confidence": "high",
    "suggestion": "Missing tables: assessments. Try asking about available data."
}
```

### Enhanced Endpoint Logic
**Location**: `backend/app/api/endpoints/ai_query.py`

**Flow**:
```
User Question
    ↓
Pre-Analysis (validate tables)
    ↓
├─ Tables Missing? → Return helpful error + suggestions
└─ Tables Available? → Generate SQL → Execute → Return results
```

## Benefits

### 1. **Prevents Errors**
- No more queries to non-existent tables
- Catches issues before SQL generation

### 2. **Better Error Messages**
Instead of:
```
"I couldn't find the specific table or data you requested"
```

Now shows:
```
"I couldn't find the necessary data to answer your question. 
The query requires tables that don't exist in the database: srec_2025_2_test_data.

Did you mean one of these tables?
- coding_results
- assessment_results

You can ask 'What tables are available?' to see all available data sources."
```

### 3. **Smarter Suggestions**
- Suggests similar table names
- Provides relevant follow-up questions
- Helps users discover available data

### 4. **Debug Visibility**
Console output shows analysis details:
```
📊 Question Analysis:
   - Query Type: complex
   - Tables Needed: ['srec_2025_2_test_data']
   - Tables Available: []
   - Tables Missing: ['srec_2025_2_test_data']
   - Can Proceed: False
   - Reasoning: Need student assessment data from college-specific table
```

## Usage Examples

### Example 1: Missing Table
**Question**: "how many assessments so far i done?"

**Analysis**:
- Tables Needed: `srec_2025_2_test_data`
- Tables Missing: `srec_2025_2_test_data`
- Can Proceed: ❌ No

**Response**:
```
I couldn't find the necessary data to answer your question. 
The query requires tables that don't exist: srec_2025_2_test_data.

Did you mean one of these tables?
- coding_results
- assessment_results
- user_assessments

You can ask 'What tables are available?' to see all available data sources.
```

### Example 2: Available Tables
**Question**: "show me all courses"

**Analysis**:
- Tables Needed: `courses`
- Tables Available: `courses`
- Can Proceed: ✅ Yes

**Response**: (Generates SQL and returns course data)

### Example 3: General Knowledge
**Question**: "what is machine learning?"

**Analysis**:
- Query Type: `general_knowledge`
- Can Proceed: ✅ Yes (no database needed)

**Response**: (Returns AI-generated answer without database query)

## Configuration

No configuration needed! The feature is automatically enabled.

## Testing

Run the test script:
```bash
cd c:\Users\Varun\Desktop\backendaionly
python test_ai_analysis.py
```

Or test via API:
```bash
curl -X POST http://localhost:8000/api/v1/ai/ask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "how many assessments so far i done?",
    "model": "deepseek-chat"
  }'
```

## Performance Impact

- **Additional API Call**: +1 AI call per question (for analysis)
- **Latency**: ~500-800ms additional (runs before SQL generation)
- **Cost**: Minimal (analysis uses fewer tokens than SQL generation)
- **Benefit**: Prevents wasted SQL generation for impossible queries

## Fallback Behavior

If the pre-analysis fails:
- System logs the error
- Proceeds with original SQL generation flow
- Ensures backward compatibility

## Future Enhancements

1. **Cache Analysis Results**: For similar questions
2. **Learn from Errors**: Track which tables users frequently request
3. **Auto-Suggest Alternatives**: Recommend similar available data
4. **Multi-Table Suggestions**: When one table is missing, suggest query rewrites

## Monitoring

Check console logs for analysis details:
```
📊 Question Analysis:
   - Query Type: complex
   - Tables Needed: ['users', 'courses']
   - Tables Available: ['users', 'courses']
   - Can Proceed: True
   - Reasoning: Join users with enrolled courses
```

## Troubleshooting

### Issue: Analysis always fails
**Solution**: Check DeepSeek API key is configured

### Issue: Wrong tables identified
**Solution**: Review the schema context in `schema_context.py`

### Issue: Too slow
**Solution**: Consider caching analysis results for common questions

## Summary

This enhancement transforms the AI from a "try and fail" approach to a "validate then execute" approach, resulting in:
- ✅ Fewer errors
- ✅ Better user experience
- ✅ More helpful error messages
- ✅ Faster debugging
- ✅ Smarter suggestions
