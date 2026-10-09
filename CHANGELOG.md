# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

***

## [Unreleased]

### Added
- CHANGELOG (this file) created and back-filled with prior changes and releases
- Included `.gitignore`
- Included unit tests:
  - `test_e_val_select.py` for the main solver engine 
  - `test_eng_notation.py` for engineering notation handling
  - `test_input_checks.py` for input validation functions

### Changed
- **BREAKING:** `e_vals.py` renamed to `e_series_solver.py`
- *Script:* Save output option only prompted once per script run, and multiple copies of the same run cannot be saved
- *Script:* No longer forces exit if a `ValueError` is caught from the solver engine, and the script can be exited or restarted
- Now prioritizes component valuess within the desired decades that have the same or less percent error
- `e_val_select()` raises descriptive exceptions if no component values were able to be solved for

### Fixed
- *Script:* Now restores text cursor after "spinner" animation in all cases
- Results printed to the terminal through `print_e_val_results()` now indicate when a percent error is nonzero and less than 0.001%
- `e_val_select()` no longer raises exception at first instance of a negative or zero component value
- Fully-determined case in `e_val_select()` now cycles through all solution sets returned by `sp.solve()` and finds the rounded solution set with the lowest cumulative error
- Component values returned from `e_val_select()` now are rounded to mitigate floating-point rounding errors

***
*All details below this point were retroactively added to the changelog.*
***

## [1.1.1] - 2026-07-29
Bug patch

### Fixed
- Under-determined case in `e_val_select()` no longer skips initial E-Series values on subsequent dictionaries if multiple solution sets are returned by `sp.solve()`


***

## [1.1.0] - 2026-07-29
UI Improvements and Bug Fixes

### Added
- *Script:* Added terminal bell (alert sound) when script calculation completes and exceeded 5 seconds
- *Script:* Added in-line "spinner" animation during script calculation to show process has not crashed
- README updated to reflect relevant fixes
- Comments added to `e_val_select()` to aid in troubleshooting and maintenance
  
### Changed
- *Script:* End-of-run menu prints `Invalid command.` when an unrecognized option is selected

### Fixed
- Engineering constants in `e_val_select()` were corrected after erroneous change in *v1.0.1*, and are now expressed unambiguously in exponential notation

***

## [1.0.1] - 2026-07-20
Bug patch

### Changed
- Updated README examples to reflect fixes

### Fixed
- Engineering notation constants in `e_val_select()` updated to correct powers of 10


***

## [1.0.0] - 2026-07-19
First stable version

### Added
- Uploaded `e_vals.py` from existing code
- Added MIT license
- Added README
- *Script:* Now can exit at any input line by typing `EXIT`, and exit message will print with exit location
- *Script:* End-of-run menu now allows entering `R` to rerun program with new values
- Added engineering notation and mathematical constants to `e_val_select()` to make relationship entry easier
- Exception raised when empty string passed as `components` in `e_val_select()`
- Added input pre-verification functions for values to be passed to `e_val_select()`
  - `component_check()` validates individual component names
  - `relationship_check()` does basic validation for relationship equation formatting
  - `e_series_selection_check()` validates E-Series selection integers
  - `decade_check()` validates decade selection numbers
  - `InvalidValueError` exception class raised by verification functions with useful error strings
- Added docstring to `save_to_textfile()`
- `eng_note()` can now print with UTF-8 characters instead of only ASCII, which can improve output readability

### Changed
- Output formatting for script
- `header` changed to `footer` in `save_to_textfile()`, and prints at bottom of file
- Multi-line `print()` statements edited to improve clarity while maintaining the same output
- Function variables assigned type hints and initialized with default values
- `decade` changed to `decade_selection` in `e_val_select()` input
- `e_series_selection` and `decade_selection` are now tuples instead of lists, in `e_val_select()`

### Fixed
- *Script:* Now at least one component must be entered before continuing to relationship entry
- *Script:* Elapsed computing time being less than one millisecond no longer causes crash
- Component string passed to `e_val_select()` can now contain at minimum one component
- Selecting `0` for `numSigFigs` passed to `eng_note()` now correctly formats with maximum length of digits
- Made passing `seriesDict` optional for `print_e_val_results()`
- Components are now assumed to be positive and real by SymPy in `e_val_select()`
- `e_val_select()` gracefully raises `ValueError` when relationship equations cannot be solved by SymPy instead of crashing
