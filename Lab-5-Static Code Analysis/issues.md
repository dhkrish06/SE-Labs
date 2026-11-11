\# Issues Found and Fixed



| Issue | Type | Line(s) | Description | Fix Approach |

|-------|------|---------|-------------|--------------|

| Mutable default argument | Bug | 9 | `zone\_records=\[]` is shared across calls | Changed default to `None` and initialized inside function |

| Bare except | Bug / Style | 16, 22, 29, 43 | Catches all exceptions | Replaced with specific exceptions (`Exception`, `KeyError`, etc.) |

| Insecure file handling | Security / Quality | 42, 47 | Used `open()` without `with` and encoding | Used `with open(..., encoding="utf-8")` |

| Invalid function name | Style | 51 | `setExpiry` does not follow snake\_case | Renamed to `set\_expiry` |

| Missing docstrings | Quality | Multiple | Functions and module had no documentation | Added module and function docstrings |

| Line too long | Style | 13, 27, 62 | Lines exceeded 79/100 characters | Broke long lines |

| Missing blank lines | Style | Multiple | PEP-8 requires 2 blank lines between functions | Added proper spacing |

