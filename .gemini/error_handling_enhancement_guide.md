# Enhanced Error Handling & Output Format - Implementation Guide

## Current Issues from Screenshot

Looking at the chat interface, I can see these error presentation issues:

1. **"Access Denied: You are restricted to your own data and Departmental Analytics."**
   - ❌ Too technical and vague
   - ❌ Doesn't explain WHY or WHAT the user can do instead

2. **"I couldn't retrieve that information from the database..."**
   - ❌ Generic error message
   - ❌ No actionable guidance
   - ❌ Doesn't suggest alternatives

3. **No visual distinction** between errors and successful responses

---

## Proposed Error Handling Strategy

### 1. **Error Categories & User-Friendly Messages**

Create distinct error types with helpful, actionable messages:

```python
class ErrorType:
    ACCESS_DENIED = "access_denied"
    DATA_NOT_FOUND = "data_not_found"
    INVALID_QUERY = "invalid_query"
    SYSTEM_ERROR = "system_error"
    NO_DATA_YET = "no_data_yet"
    PERMISSION_SCOPE = "permission_scope"

ERROR_MESSAGES = {
    # Access Denied Errors
    "access_denied_other_college": {
        "title": "Access Restricted",
        "message": "You can only access data from your college ({college_name}). The information you requested belongs to a different institution.",
        "icon": "🔒",
        "suggestions": [
            "View your college's performance metrics",
            "Show department-wise statistics",
            "See student enrollment in your college"
        ]
    },
    
    "access_denied_other_student": {
        "title": "Privacy Protection",
        "message": "For privacy reasons, you can only view your own academic records. Other students' individual data is protected.",
        "icon": "🔒",
        "suggestions": [
            "View your own performance",
            "See department leaderboard (names only)",
            "Compare your rank with department average"
        ]
    },
    
    "access_denied_other_department": {
        "title": "Department Access Restricted",
        "message": "You can only access data from your department ({dept_name}). This helps maintain data privacy across departments.",
        "icon": "🔒",
        "suggestions": [
            "View your department's performance",
            "See students in your department",
            "Show your department's rankings"
        ]
    },
    
    # Data Not Found Errors
    "data_not_found_table": {
        "title": "Data Not Available",
        "message": "The specific information you're looking for hasn't been recorded in the system yet. This could be because assessments haven't been conducted or results haven't been uploaded.",
        "icon": "📊",
        "suggestions": [
            "Check available courses",
            "View your enrolled courses",
            "See upcoming assessments"
        ]
    },
    
    "data_not_found_no_results": {
        "title": "No Results Found",
        "message": "I searched the database but couldn't find any matching records. This might be because the data hasn't been entered yet or the filters are too specific.",
        "icon": "🔍",
        "suggestions": [
            "Try a broader search",
            "Check if the course/assessment exists",
            "View all available data"
        ]
    },
    
    # No Data Yet (Student-specific)
    "no_assessment_data": {
        "title": "No Assessment Data Yet",
        "message": "You haven't attempted any assessments in this course yet. Once you start solving problems, I'll be able to analyze your performance and provide personalized recommendations.",
        "icon": "📝",
        "suggestions": [
            "View available assessments",
            "See course details",
            "Start practicing questions"
        ]
    },
    
    # System Errors
    "system_error_sql": {
        "title": "Technical Issue",
        "message": "I encountered a technical problem while retrieving your data. Our team has been notified and will fix this soon.",
        "icon": "⚠️",
        "suggestions": [
            "Try rephrasing your question",
            "Ask about a different topic",
            "Contact support if this persists"
        ]
    },
    
    # Invalid Query
    "invalid_query_unclear": {
        "title": "I Need More Details",
        "message": "I'm not sure exactly what you're looking for. Could you provide more specific details?",
        "icon": "❓",
        "suggestions": [
            "Specify the course or subject",
            "Mention the time period (e.g., this semester)",
            "Clarify what metric you want (e.g., marks, rank, count)"
        ]
    }
}
```

---

### 2. **Enhanced Response Format**

Create a structured response format that's easy to parse on the frontend:

```python
class EnhancedResponse:
    def __init__(self):
        self.status = "success"  # success, error, warning, info
        self.type = None  # error_type if status is error
        self.title = None  # Short title for the response
        self.answer = ""  # Main answer text
        self.icon = None  # Emoji or icon identifier
        self.data = None  # Structured data if available
        self.suggestions = []  # Follow-up suggestions
        self.metadata = {}  # Additional context
        
    def to_dict(self):
        return {
            "status": self.status,
            "type": self.type,
            "title": self.title,
            "answer": self.answer,
            "icon": self.icon,
            "data": self.data,
            "follow_ups": self.suggestions,
            "metadata": self.metadata
        }
```

---

### 3. **Error Detection & Classification**

Implement smart error detection:

```python
def classify_error(error_message: str, question: str, user_role: int, generated_sql: str) -> dict:
    """
    Classify the error and return appropriate user-friendly message
    """
    error_lower = error_message.lower()
    question_lower = question.lower()
    
    # Table doesn't exist
    if "doesn't exist" in error_lower or "unknown table" in error_lower:
        # Extract table name from error
        import re
        table_match = re.search(r"table ['\"]?(\w+)['\"]?", error_lower)
        table_name = table_match.group(1) if table_match else "requested"
        
        return {
            "error_type": "data_not_found_table",
            "context": {"table_name": table_name}
        }
    
    # No results returned (empty dataset)
    if "no results" in error_lower or "empty" in error_lower:
        return {
            "error_type": "data_not_found_no_results",
            "context": {}
        }
    
    # Column doesn't exist
    if "unknown column" in error_lower or "column" in error_lower and "not found" in error_lower:
        return {
            "error_type": "system_error_sql",
            "context": {"technical_detail": "Column mismatch"}
        }
    
    # Syntax error (AI generated bad SQL)
    if "syntax error" in error_lower or "sql syntax" in error_lower:
        return {
            "error_type": "system_error_sql",
            "context": {"technical_detail": "Query syntax issue"}
        }
    
    # Default
    return {
        "error_type": "system_error_sql",
        "context": {}
    }
```

---

### 4. **Context-Aware Error Messages**

Customize error messages based on user context:

```python
def get_contextual_error_message(
    error_type: str,
    user_role: int,
    college_name: str = None,
    dept_name: str = None,
    context: dict = None
) -> dict:
    """
    Get error message customized for user's role and context
    """
    base_error = ERROR_MESSAGES.get(error_type, ERROR_MESSAGES["system_error_sql"])
    
    # Customize message with user context
    message = base_error["message"]
    if "{college_name}" in message and college_name:
        message = message.format(college_name=college_name)
    if "{dept_name}" in message and dept_name:
        message = message.format(dept_name=dept_name)
    
    # Customize suggestions based on role
    suggestions = base_error["suggestions"]
    if user_role == 7:  # Student
        suggestions = [s for s in suggestions if "your" in s.lower() or "my" in s.lower()]
    elif user_role == 3:  # College Admin
        suggestions = [s for s in suggestions if "college" in s.lower() or "department" in s.lower()]
    
    return {
        "title": base_error["title"],
        "message": message,
        "icon": base_error["icon"],
        "suggestions": suggestions
    }
```

---

### 5. **Implementation in ai_query.py**

Here's how to integrate this into your existing code:

```python
# After SQL execution fails (around line 295)
if "error" in execution_result:
    # Enhanced logging for debugging
    print(f"❌ SQL EXECUTION ERROR:")
    print(f"   Question: {question}")
    print(f"   Generated SQL: {generated_sql}")
    print(f"   Error: {execution_result.get('error', 'Unknown error')}")
    
    # Classify the error
    error_classification = classify_error(
        error_message=execution_result.get('error', ''),
        question=question,
        user_role=current_role_id,
        generated_sql=generated_sql
    )
    
    # Get contextual error message
    error_response = get_contextual_error_message(
        error_type=error_classification["error_type"],
        user_role=current_role_id,
        college_name=college_name if current_role_id in [3, 7] else None,
        dept_name=dept_name if current_role_id in [4, 5, 7] else None,
        context=error_classification.get("context", {})
    )
    
    # Return enhanced error response
    return {
        "status": "error",
        "type": error_classification["error_type"],
        "title": error_response["title"],
        "answer": error_response["message"],
        "icon": error_response["icon"],
        "follow_ups": error_response["suggestions"],
        "metadata": {
            "error_category": error_classification["error_type"],
            "timestamp": datetime.now().isoformat()
        }
    }
```

---

### 6. **Access Denied Enhancement**

Make access denied messages more helpful:

```python
# Replace lines 273-290 with:
if "ACCESS_DENIED_VIOLATION" in generated_sql:
    # Determine specific access denial reason
    question_lower = question.lower()
    
    # Check if asking about other college
    if any(college_keyword in question_lower for college_keyword in ["skct", "skcet", "other college"]):
        error_type = "access_denied_other_college"
    # Check if asking about other student
    elif any(name_indicator in question_lower for name_indicator in ["show", "marks of", "performance of"]):
        error_type = "access_denied_other_student"
    # Check if asking about other department
    elif "department" in question_lower and current_role_id in [4, 5, 7]:
        error_type = "access_denied_other_department"
    else:
        error_type = "access_denied_generic"
    
    # Get contextual message
    error_response = get_contextual_error_message(
        error_type=error_type,
        user_role=current_role_id,
        college_name=college_name,
        dept_name=dept_name
    )
    
    return {
        "status": "error",
        "type": "access_denied",
        "title": error_response["title"],
        "answer": error_response["message"],
        "icon": error_response["icon"],
        "follow_ups": error_response["suggestions"]
    }
```

---

### 7. **Frontend Display Recommendations**

For the frontend to display these errors beautifully:

```typescript
// Frontend component
interface ErrorResponse {
  status: 'error' | 'success' | 'warning' | 'info';
  type: string;
  title: string;
  answer: string;
  icon: string;
  follow_ups: string[];
  metadata?: any;
}

function renderResponse(response: ErrorResponse) {
  if (response.status === 'error') {
    return (
      <div className="error-card">
        <div className="error-header">
          <span className="error-icon">{response.icon}</span>
          <h3 className="error-title">{response.title}</h3>
        </div>
        <p className="error-message">{response.answer}</p>
        <div className="error-suggestions">
          <p className="suggestions-label">You can try:</p>
          <ul>
            {response.follow_ups.map((suggestion, i) => (
              <li key={i} onClick={() => askQuestion(suggestion)}>
                {suggestion}
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }
  
  // Regular success response
  return <div className="success-card">...</div>;
}
```

---

### 8. **CSS Styling Recommendations**

```css
.error-card {
  background: linear-gradient(135deg, #fff5f5 0%, #fff 100%);
  border-left: 4px solid #e53e3e;
  border-radius: 8px;
  padding: 16px;
  margin: 12px 0;
}

.error-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.error-icon {
  font-size: 24px;
}

.error-title {
  color: #c53030;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.error-message {
  color: #2d3748;
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 16px 0;
}

.error-suggestions {
  background: white;
  border-radius: 6px;
  padding: 12px;
}

.suggestions-label {
  font-size: 13px;
  font-weight: 500;
  color: #4a5568;
  margin: 0 0 8px 0;
}

.error-suggestions ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.error-suggestions li {
  padding: 8px 12px;
  margin: 4px 0;
  background: #f7fafc;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 13px;
  color: #2b6cb0;
}

.error-suggestions li:hover {
  background: #ebf8ff;
  transform: translateX(4px);
}
```

---

### 9. **Success Response Enhancement**

Also enhance successful responses for consistency:

```python
def format_success_response(answer: str, data: list, question: str, role_id: int) -> dict:
    """
    Format successful responses with enhanced structure
    """
    # Detect response type
    if any(keyword in question.lower() for keyword in ["how many", "count", "total"]):
        response_type = "count"
        icon = "📊"
    elif any(keyword in question.lower() for keyword in ["rank", "position", "standing"]):
        response_type = "ranking"
        icon = "🏆"
    elif any(keyword in question.lower() for keyword in ["performance", "marks", "score"]):
        response_type = "performance"
        icon = "📈"
    elif any(keyword in question.lower() for keyword in ["list", "show", "display"]):
        response_type = "list"
        icon = "📋"
    else:
        response_type = "general"
        icon = "💡"
    
    return {
        "status": "success",
        "type": response_type,
        "title": None,  # No title needed for success
        "answer": answer,
        "icon": icon,
        "data": data if len(data) < 100 else None,  # Don't send huge datasets
        "follow_ups": generate_smart_followups(question, data, role_id),
        "metadata": {
            "result_count": len(data),
            "timestamp": datetime.now().isoformat()
        }
    }
```

---

### 10. **Error Logging & Monitoring**

Add structured logging for error tracking:

```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def log_error(
    error_type: str,
    question: str,
    user_id: int,
    user_role: int,
    error_details: dict
):
    """
    Log errors in structured format for monitoring
    """
    logger.error(
        "AI Query Error",
        extra={
            "error_type": error_type,
            "question": question,
            "user_id": user_id,
            "user_role": user_role,
            "timestamp": datetime.now().isoformat(),
            "details": error_details
        }
    )
    
    # Optional: Send to monitoring service (e.g., Sentry, DataDog)
    # sentry_sdk.capture_message(f"AI Query Error: {error_type}")
```

---

## Implementation Priority

### Phase 1: Quick Wins (1-2 hours)
1. ✅ Create ERROR_MESSAGES dictionary
2. ✅ Implement classify_error() function
3. ✅ Update access denied handling
4. ✅ Add error logging

### Phase 2: Enhanced Responses (2-3 hours)
1. ✅ Implement get_contextual_error_message()
2. ✅ Update all error return statements
3. ✅ Add success response formatting
4. ✅ Test with various error scenarios

### Phase 3: Frontend Integration (2-4 hours)
1. ✅ Update frontend to handle new response format
2. ✅ Add CSS styling for error cards
3. ✅ Implement clickable suggestions
4. ✅ Add loading states and transitions

---

## Example: Before vs After

### Before
```json
{
  "answer": "Access Denied: You are restricted to your own data and Departmental Analytics.",
  "follow_ups": []
}
```

### After
```json
{
  "status": "error",
  "type": "access_denied_other_student",
  "title": "Privacy Protection",
  "answer": "For privacy reasons, you can only view your own academic records. Other students' individual data is protected.",
  "icon": "🔒",
  "follow_ups": [
    "View your own performance",
    "See department leaderboard (names only)",
    "Compare your rank with department average"
  ],
  "metadata": {
    "error_category": "access_denied",
    "timestamp": "2026-02-17T14:18:16+05:30"
  }
}
```

---

## Testing Checklist

Test these error scenarios:

- [ ] Access denied (other college)
- [ ] Access denied (other student)
- [ ] Access denied (other department)
- [ ] Table doesn't exist
- [ ] No results found
- [ ] No assessment data yet
- [ ] SQL syntax error
- [ ] Column doesn't exist
- [ ] Permission denied
- [ ] Invalid query

---

**Next Steps**: Would you like me to implement this error handling system in your codebase?
