#  Static Code Analysis – Cleaned Inventory System

## Known Issue Table 

| **Priority** | **Issue** | **Type** | **Line(s)** | **Description** | **Fix Approach** |
|---------------|------------|-----------|--------------|------------------|------------------|
| **High** | Use of `eval()` | Security | Bottom of file | Dangerous — allows arbitrary code execution, potential security vulnerability. | Removed `eval()` completely and replaced with a safe `logging.debug()` message. |
| **High** | Bare `except:` clause | Logic / Security | Multiple | Caught all exceptions blindly, masking real errors. | Replaced with specific exception types like `FileNotFoundError`, `ValueError`, `TypeError`, and `KeyError`. |
| **High** | Missing input validation (`item`, `qty`) | Logic / Validation | `add_item()`, `remove_item()` | Allowed invalid types or negative quantities. | Added explicit type and value validation using `TypeError` and `ValueError`. |
| **Medium** | Mutable default argument (`logs=[]`) | Bug | `add_item()` definition | Lists as default parameters cause shared state across calls. | Changed default to `None` and initialized inside function. |
| **Medium** | Improper file handling | Maintainability | `load_data()`, `save_data()` | Opened files without `with`, risking unclosed handles. | Used `with open(...)` for safe automatic closure. |
| **Low** | Missing main guard | Style / Safety | End of file | Script executed automatically when imported. | Wrapped main logic in `main()` and added `if __name__ == "__main__":`. |
| **Low** | Poor output handling | Code Quality | Throughout | Used `print()` instead of proper logging. | Replaced with Python’s `logging` module for consistent, configurable logs. |
| **Low** | PEP8 formatting violations (E501, spacing) | Style | Multiple | Lines exceeded 79 characters or spacing inconsistent. | Reformatted to align with PEP8 guidelines or added `.flake8` config to allow 100 chars. |

---

##  Reflection Questions and Answers

### 1 Which issues were the easiest to fix, and which were the hardest? Why?
The easiest issues to fix were the **PEP8 formatting violations** and the **mutable default argument**.  
They required only structural or syntactic changes.  
The hardest were **exception handling** and **input validation**, since they needed logical restructuring and careful testing to avoid breaking program behavior.

---

### 2 Did the static analysis tools report any false positives? If so, describe one example.
Yes. **Pylint** flagged some variables as “unused” when they were used only within logging statements.  
These are **false positives**, as they serve a purpose for debugging and traceability.

---

### 3 How would you integrate static analysis tools into your actual software development workflow?
I would integrate **Pylint**, **Flake8**, and **Bandit** into a **Continuous Integration (CI)** pipeline (for example, using GitHub Actions).  
They would automatically run on every commit or pull request, ensuring that no new code introduces quality, style, or security regressions.  
Locally, I’d configure my IDE to run them on save or before commits.

---

### 4 What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?
After the fixes:
- The code became **safer and cleaner** with no security warnings.  
- **Logging** made tracing easier and eliminated print clutter.  
- **Input validation** prevented crashes and logic errors.  
- **PEP8 compliance** improved readability and professional appearance.  
Overall, the cleaned file is now more robust, maintainable, and aligned with real-world software engineering standards.

---

**Date Completed:** October 27, 2025  
**Author:** Gourav Kumar D
