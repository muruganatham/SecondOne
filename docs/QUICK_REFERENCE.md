# Quick Reference: AI Pre-Analysis Feature

## What Changed?

### Before ❌
```
User asks question → AI generates SQL → SQL fails → Generic error message
```

### After ✅
```
User asks question → AI analyzes tables → Validates availability → 
  ├─ Missing tables? → Helpful error + suggestions
  └─ Tables exist? → Generate SQL → Execute → Return results
```

## How to Use

### 1. Normal Usage (No Changes Required)
Just ask questions as usual:
```bash
curl -X POST http://localhost:8000/api/v1/ai/ask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "how many students are enrolled?", "model": "deepseek-chat"}'
```

### 2. Check Available Tables
```bash
curl -X GET http://localhost:8000/api/v1/ai/tables \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Monitor Analysis (Console Logs)
Watch your backend console for:
```
📊 Question Analysis:
   - Query Type: complex
   - Tables Needed: ['users', 'courses']
   - Tables Available: ['users', 'courses']
   - Can Proceed: True
   - Reasoning: Join users with enrolled courses
```

## Error Messages

### Old Error (Confusing)
```json
{
  "answer": "I couldn't find the specific table or data you requested in the current database.",
  "sql": "SELECT COUNT(*) FROM non_existent_table WHERE user_id = 123",
  "data": []
}
```

### New Error (Helpful)
```json
{
  "answer": "I couldn't find the necessary data to answer your question. The query requires tables that don't exist in the database: non_existent_table.\n\nDid you mean one of these tables?\n- users\n- user_data\n- user_profiles\n\nYou can ask 'What tables are available?' to see all available data sources.",
  "sql": "-- Analysis: Missing tables: non_existent_table",
  "data": [],
  "follow_ups": ["What tables are available?", "Show me available data", "List all courses"]
}
```

## Files Modified

1. **`backend/app/services/ai_service.py`**
   - Added `analyze_question_and_tables()` method
   - Pre-validates table availability

2. **`backend/app/api/endpoints/ai_query.py`**
   - Added pre-analysis step before SQL generation
   - Enhanced error handling with suggestions

## Testing

### Test Script
```bash
cd c:\Users\Varun\Desktop\backendaionly
python test_ai_analysis.py
```

### Manual Test
```bash
# Test with missing table
curl -X POST http://localhost:8000/api/v1/ai/ask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "show data from fake_table", "model": "deepseek-chat"}'

# Test with existing table
curl -X POST http://localhost:8000/api/v1/ai/ask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type": "application/json" \
  -d '{"question": "show all courses", "model": "deepseek-chat"}'
```

## Troubleshooting

### Issue: Still getting generic errors
**Cause**: Server didn't reload with new code
**Solution**: Restart the server
```bash
# Stop current server (Ctrl+C)
# Restart
uvicorn app.main:app --reload --host 0.0.0.0
```

### Issue: Analysis takes too long
**Cause**: DeepSeek API latency
**Solution**: This is normal (~500-800ms), prevents wasted SQL generation

### Issue: Wrong tables identified
**Cause**: Schema context might be outdated
**Solution**: Check `backend/database_analysis/` files are up to date

## Benefits Summary

| Aspect | Before | After |
|--------|--------|-------|
| Error Rate | High (frequent table not found errors) | Low (caught before SQL generation) |
| Error Messages | Generic, unhelpful | Specific, actionable |
| User Experience | Frustrating | Guided and helpful |
| Debug Time | Long (unclear what went wrong) | Short (clear analysis logs) |
| Suggestions | None | Similar tables + follow-ups |

## Next Steps

1. ✅ **Feature is live** - No action needed
2. 📊 **Monitor logs** - Check console for analysis details
3. 🧪 **Test queries** - Try questions that previously failed
4. 📈 **Track improvements** - Note reduction in errors

## Support

For issues or questions:
1. Check console logs for analysis details
2. Review `docs/AI_PRE_ANALYSIS.md` for full documentation
3. Test with `test_ai_analysis.py` script

---

**Last Updated**: 2026-02-11
**Version**: 1.0
**Status**: ✅ Active
