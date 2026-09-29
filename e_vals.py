"""
This module contains functions to calculate the best E-series component values 
based on mathematical relationships between components.

NOTE: SymPy is a dependency and must be installed to run.

Instead of calling the functions directly, the module can be run as a script
and the values can be entered when prompted.
The results will be written to the screen.

"""


import sys
from time import time, ctime, sleep
from math import log10

try:
    import sympy as sp
except ModuleNotFoundError:
    print("\033[1;31;40mSymPy must be installed to run.\nPlease run \
          \033[0mpip install sympy\033[1;31;40m in the terminal.\033[0m")
    print("\033[1;31;40mPress \033[0m[ENTER]\033[1;31;40m to exit.\033[0m")
    input()
    sys.exit(1)


#################################   CALLABLE FUNCTIONS   #################################

    

def e_val_select(components: str, relationships: list, e_series_selection: tuple, decade_selection: tuple) -> dict:
    """
    Finds E-series of preferred numbers values for components based on mathematical relationships.
    This function will identify the values that minimize error between the real values and the E-series values.
    The module "SymPy" is a dependency. Run "pip install sympy" in the command prompt to install.
    
    Args:
        components (str):           Names of components, as a string delimited with spaces.
                                    Example: "R1 R2 C1 L1"
        relationships (list):       List of strings representing mathematical relationships of the components.
                                    Example: ["R2 / R1 = 2", "1 / (C1 * L1) = 500", "(R1 + R2) / (C1 + L1) = 2"]
        e_series_selection (tuple): List of E-series to use for each component, in the same order as "components".
                                    Must be 3, 6, 12, 24, 48, 96, or 192.
                                    Example: (24, 24, 12, 6)
                                            For R1 to be in E24, R2 in E24, C1 in E12, and L1 in E6.
        decade_selection (tuple):   List of preferrred decade value for each component's E-series values, in the same 
                                    order as "components".
                                    Since it cannot be predicted what component SymPy will initially solve for,
                                    not all components may be within their preferred decade.
                                    This value can either be a float or a string in engineering notation.
                                    Example: (1000, '10k', 0.000001, '100u')
                                             For R1 to be within 1k, R2 within 10k, C1 within 1µ, and L1 within 200µ.
    
    Returns:
        Dictionary, with component names as keys, and tuple containing (VALUE, ERROR) as values.
        'VALUE' is the calculated E-Series value, and 'ERROR' is the percent error between the E-Series value and the ideal.
    """
    e_series_array = []
    for item in e_series_selection:
        match item:
            case 3:                                                         # E-3
                e_vals = [1.0, 2.2, 4.7]
            case 6:                                                         # E-6
                e_vals = [1.0, 1.5, 2.2, 3.3, 4.7, 6.8]
            case 12:                                                        # E-12
                e_vals = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 
                          3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
            case 24:                                                        # E-24
                e_vals = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 
                          1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 
                          3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 
                          5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
            case 48:                                                        # E-48
                e_vals = [1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 
                          1.47, 1.54, 1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 
                          2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01, 
                          3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 
                          4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49, 
                          6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53]
            case 96:                                                        # E-96
                e_vals = [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 
                          1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 
                          1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 
                          1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 
                          2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 
                          2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 
                          3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 
                          3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 
                          4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 
                          5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 
                          6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 
                          8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76]
            case 192:                                                       # E-192
                e_vals = [1.00, 1.01, 1.02, 1.04, 1.05, 1.06, 1.07, 1.09, 
                          1.10, 1.11, 1.13, 1.14, 1.15, 1.17, 1.18, 1.20, 
                          1.21, 1.23, 1.24, 1.26, 1.27, 1.29, 1.30, 1.32, 
                          1.33, 1.35, 1.37, 1.38, 1.40, 1.42, 1.43, 1.45, 
                          1.47, 1.49, 1.50, 1.52, 1.54, 1.56, 1.58, 1.60, 
                          1.62, 1.64, 1.65, 1.67, 1.69, 1.72, 1.74, 1.76, 
                          1.78, 1.80, 1.82, 1.84, 1.87, 1.89, 1.91, 1.93, 
                          1.96, 1.98, 2.00, 2.03, 2.05, 2.08, 2.10, 2.13, 
                          2.15, 2.18, 2.21, 2.23, 2.26, 2.29, 2.32, 2.34, 
                          2.37, 2.40, 2.43, 2.46, 2.49, 2.52, 2.55, 2.58, 
                          2.61, 2.64, 2.67, 2.71, 2.74, 2.77, 2.80, 2.84, 
                          2.87, 2.91, 2.94, 2.98, 3.01, 3.05, 3.09, 3.12, 
                          3.16, 3.20, 3.24, 3.28, 3.32, 3.36, 3.40, 3.44, 
                          3.48, 3.52, 3.57, 3.61, 3.65, 3.70, 3.74, 3.79, 
                          3.83, 3.88, 3.92, 3.97, 4.02, 4.07, 4.12, 4.17, 
                          4.22, 4.27, 4.32, 4.37, 4.42, 4.48, 4.53, 4.59, 
                          4.64, 4.70, 4.75, 4.81, 4.87, 4.93, 4.99, 5.05, 
                          5.11, 5.17, 5.23, 5.30, 5.36, 5.42, 5.49, 5.56, 
                          5.62, 5.69, 5.76, 5.83, 5.90, 5.97, 6.04, 6.12, 
                          6.19, 6.26, 6.34, 6.42, 6.49, 6.57, 6.65, 6.73, 
                          6.81, 6.90, 6.98, 7.06, 7.15, 7.23, 7.32, 7.41, 
                          7.50, 7.59, 7.68, 7.77, 7.87, 7.96, 8.06, 8.16, 
                          8.25, 8.35, 8.45, 8.56, 8.66, 8.76, 8.87, 8.98, 
                          9.09, 9.20, 9.31, 9.42, 9.53, 9.65, 9.76, 9.88]
                
        e_series_array.append(e_vals)   # Make list of E-Series value lists, in order of 'e_series_selection'
    
    decade = []
    for value in decade_selection:              # Convert all 'decade_selection' values to floats, and place in 'decade'
        decade.append(eng_to_float(str(value)))

    symList = components.split() # Seperate string of components into list
    if len(symList) == 0:
        raise ValueError("No Components were passed. Unable to continue.")
    elif len(symList) == 1:
        syms = (sp.symbols(components, positive=True, real=True), )   #Formatting as tuple with one element
    else:
        syms = sp.symbols(components, positive=True, real=True)
    
    constants = {  # Pre-determined values to make equation entry simpler
        ###CONSTANTS
        sp.Symbol('pi'):        3.14159265358979323846264338327950,
        sp.Symbol('e'):         2.71828182845904523536028747135266,
        sp.Symbol('phi'):       1.61803398874989484820458683436563,
        sp.Symbol('sqrt_2', 
        pretty_name='\u221A2'): 1.41421356237309504880168872420969,
        sp.Symbol('sqrt_3', 
        pretty_name='\u221A3'): 1.73205080756887729352744634150587,
        
        ### ENGINEERING NOTATION
        sp.Symbol('Y'):        10**24,
        sp.Symbol('Z'):        10**21,
        sp.Symbol('E'):        10**18,
        sp.Symbol('P'):        10**15,
        sp.Symbol('T'):        10**12,
        sp.Symbol('G'):        10**9,
        sp.Symbol('M'):        10**6,
        sp.Symbol('k'):        10**3,
        sp.Symbol('m'):        10**-3,
        sp.Symbol('u',
        pretty_name='\u03BC'): 10**-6,
        sp.Symbol('n'):        10**-9,
        sp.Symbol('p'):        10**-12,
        sp.Symbol('f'):        10**-15,
        sp.Symbol('a'):        10**-18,
        sp.Symbol('z'):        10**-21,
        sp.Symbol('y'):        10**-24}
    # Concatenate dictionaries of symbols and constants for substitution
    local_dict = {s.name: s for s in syms} | {c.name: c for c in constants.keys()} 

    equation_list = []
    # Make list of equations by seperating at '=' and parsing with SymPy
    for relationship in relationships:
        left, right = relationship.split('=')

        relat_ex = sp.parse_expr(right, local_dict=local_dict).subs(constants)
        relat_eq = sp.parse_expr(left, local_dict=local_dict).subs(constants)
        equation = sp.Eq(relat_ex, relat_eq)
        
        equation_list.append(equation)

    # Create dictionary of equations solved for a component
    value_dict = sp.solve(equation_list, syms, dict=True, rational=True, manual=True)
    if not value_dict:
        value_dict = sp.solve(equation_list, syms, dict=True, rational=True, manual=False)
        if not value_dict:
            raise ValueError("The system of component relationship equations cannot be solved.")

    values = {}
    errors = {}
    base_syms = []
    sym_index = []
    sym_incre = []

    # Create structures to track free variables and solver indexing
    for sym in syms:
        if sym not in value_dict[0]:
            base_syms.append(sym)   # List of free variables
            sym_index.append(0)     # List of indicies
            sym_incre.append(False) # List of 'index' tags

    ### FULLY DETERMINED - Round each component to nearest E-Series value per dictionary
    if not base_syms:
        negativeComponent = False
        zeroComponent = False
        skip = False
        pct_diff_sum = float('inf')
        for val_dict in value_dict:
            temp_val_dict = {}
            temp_pct_diff_dict = {}
            for sym in syms:
                raw = float(val_dict[sym])
                if raw < 0:
                    negativeComponent = True
                    skip = True
                    break
                elif raw == 0:
                    zeroComponent = True
                    skip = True
                    break

                exponent = 0
                while abs(raw) < 1:
                    exponent -= 1
                    raw = raw * 10
                    
                while abs(raw) >= 10:
                    exponent += 1
                    raw = raw / 10
                
                rounded = min(e_series_array[syms.index(sym)], key=lambda x: abs(x - raw))  # Rounding to E-Series
                
                raw = raw * 10**exponent
                if exponent < 0:
                    rounded = round(rounded * 10**exponent, abs(exponent)+2)
                else:
                    rounded = round(rounded * 10**exponent, 2)
                
                err = abs(rounded - raw)/raw
    
                temp_val_dict[sym] = rounded
                temp_pct_diff_dict[sym] = err

            if skip:
                skip = False
                continue
            temp_pct_diff_sum = 0
            for key in temp_pct_diff_dict:
                temp_pct_diff_sum += temp_pct_diff_dict[key]
            
            if temp_pct_diff_sum < pct_diff_sum:
                pct_diff_sum = temp_pct_diff_sum
                for key in temp_val_dict:
                    values[key] = temp_val_dict[key]
                    errors[key] = temp_pct_diff_dict[key]

        # These errors should not fire because of "positive=True" in sp.solve()  
        # They have been retained just in case a system sneaks through sp.solve()              
        if not values and (negativeComponent and zeroComponent):
            raise ValueError("Negative and zero component values detected. No real solution.")
        elif not values and negativeComponent:
            raise ValueError("Negative component value detected. No real solution.")
        elif not values and zeroComponent:
            raise ValueError("Component value of zero detected. No real solution.")

    ### UNDER-DETERMINED - 
    else:
        negativeComponent = False
        zeroComponent = False
        skip = False
        pct_diff_sum = float('inf')
        for val_dict in value_dict:     #For every dictionary returned by Sympy in sp.solve()
            sym_incre[0] = False        # Flags the first base symbol to start at "1.0" for each dictionary sweep
            Run = True
            while Run:
                base_syms_vals = {}
                for base_sym in base_syms:
                        base_index = base_syms.index(base_sym)
                        series_index = sym_index[base_index]
                        index = syms.index(base_sym)
                        if sym_incre[base_index]:                           # If the current base symbol is flagged to increment
                            sym_incre[base_index] = False                   #   Reset the flag
                            series_index += 1                               #   Increment the index by 1
                            if series_index >= len(e_series_array[index]):  #   If index is incremented outside of e-series value list
                                series_index = 0                            #       Set index to 0
                                if base_index + 1 < len(sym_incre):         #       If not last item in sym_incre list
                                    sym_incre[base_index+1] = True          #           Set the flag so the next base symbol index increments
                                else:                                       #       Else
                                    Run = False                             #           Reset flag to continue loop
                            sym_index[base_index] = series_index
                        val = e_series_array[index][series_index]
                        val = val * decade[index]
                        base_syms_vals[base_sym] = val
                sym_incre[0] = True    # Flags the first base symbol to increment after the first run

                if not Run:
                    break

                temp_val_dict = {}
                temp_pct_diff_dict = {}
                for key in val_dict:
                    raw = val_dict[key].evalf(subs=base_syms_vals)

                    if raw < 0:
                        skip = True
                        negativeComponent = True
                        break
                    elif raw == 0:
                        skip = True
                        zeroComponent = True
                        break
                    
                    exponent = 0
                    while abs(raw) < 1:
                        exponent -= 1
                        raw = raw * 10
                        
                    while abs(raw) >= 10:
                        exponent += 1
                        raw = raw / 10
                        
                    rounded = min(e_series_array[syms.index(key)], key=lambda x: abs(x - raw))  # Rounding to E-Series
                    
                    raw = raw * 10**exponent
                    if exponent < 0:
                        rounded = round(rounded * 10**exponent, abs(exponent)+2)
                    else:
                        rounded = round(rounded * 10**exponent, 2)
                    
                    temp_val_dict[key] = rounded
                    
                    temp_pct_diff_dict[key] = abs(rounded - raw)/raw

                if skip:
                    skip = False
                    continue
                temp_pct_diff_sum = 0
                for key in temp_pct_diff_dict:
                    temp_pct_diff_sum += temp_pct_diff_dict[key]
                
                if temp_pct_diff_sum < pct_diff_sum:
                    pct_diff_sum = temp_pct_diff_sum
                    for key in base_syms_vals:
                        values[key] = base_syms_vals[key]
                        errors[key] = 0
                    for key in temp_val_dict:
                        values[key] = temp_val_dict[key]
                        errors[key] = temp_pct_diff_dict[key]
        # These errors should not fire because of "positive=True" in sp.solve()  
        # They have been retained just in case a system sneaks through sp.solve()    
        if not values and (negativeComponent and zeroComponent):
            raise ValueError("Negative and zero component values detected. Unable to solve.")
        elif not values and negativeComponent:
            raise ValueError("Negative component values detected. Unable to solve.")
        elif not values and zeroComponent:
            raise ValueError("Component values of zero detected. Unable to solve.")
    
    if not values:
        raise ValueError("No valid component values detected. Unable to solve.")
    
    returnDict = {}
    for sym in syms:
        returnDict[symList[syms.index(sym)]] = (values[sym], errors[sym])

    return returnDict



def print_e_val_results(valueDict: dict, seriesDict: dict=None) -> None:
    """
    Prints the results of e_val_select() to terminal for display.

    Args:
        valueDict:  Dictionary of component names and values, returned from e_val_select()
        seriesDict: Dictionary of component names and component E-series values in {COMPONENT NAME : E-SERIES} pairs.
                    Only used to select the appropriate number of significant figures for display, so not necessary. 
                    Defaults to None.
        
        Returns:
            After printing to the terminal, None.
    """

    print("\033[1;36;40m┌───────────────────────────────────────┐\033[0m\n"
          "\033[1;36;40m│            R E S U L T S :            │\033[0m\n"
          "\033[1;36;40m└───────────────────────────────────────┘\033[0m")

    for component in valueDict:
        if seriesDict and component in seriesDict:
            if seriesDict[component] in [3, 6, 12, 24]:
                sigfigs = 2
            else:
                sigfigs = 3
        else:
            sigfigs = 3
        error = valueDict[component][1] * 100
        if error == 0.0:
            pct_error = "  0    "
        elif error < 0.001:
            pct_error = "< 0.001"
        else:
            pct_error = f" {error:>6.3f}"
        print(f"\033[1;33;40m{component}:\033[0m {eng_note(valueDict[component][0], sigfigs, encoding=sys.getdefaultencoding())}"
              f"\t\t\033[1;36;40mError:\033[0m {pct_error} %")

    return None
    
        

def eng_note(inputValue: float, numSigFigs: int=0, encoding: str="ASCII") -> str:
    """
    Formats a numeric value as a string in engineering notation.
    Works from -10^24 to 10^24, otherwise defaults to scientific notation.
    Using the same number of significant figures results in a consistent string length.

    Args:
        inputValue (float): numeric value to be formatted.
        numSigFigs (int):   Number of significant figures. 
                            Inputting zero results in maximum length.
                            Defaults to zero.
        encoding (str):     Selects encoding style for "micro" designation.
                            encoding="ASCII": "micro" is written as "u"
                            encoding="UTF-8": "micro" is written as "µ"
                            Default: "ASCII"
    Returns:
        String formatted in engineering notation.
    """
    exponent = 0
    newVal = float(inputValue)
    if newVal == 0:
        return f"{'0  ':>{numSigFigs+1}}"
    elif newVal == float('inf'):
        if encoding.upper() == "UTF-8":
            return f"\u221E{'  ':>{numSigFigs+1}}"
        else:
            return f"{'inf  ':>{numSigFigs+1}}"
    elif newVal == float('-inf'):
        if encoding.upper() == "UTF-8":
            return f"-\u221E{'  ':>{numSigFigs+1}}"
        else:   
            return f"{'-inf  ':>{numSigFigs+1}}"
    
    while (abs(newVal) >= 1000) and exponent <= 24:
        exponent += 3
        newVal = float(inputValue) / 10**exponent
    while (abs(newVal) < 1.0 )  and exponent >= -24:
        exponent -= 3
        newVal = float(inputValue) / 10**exponent
    
    temp_exp = 0
    match numSigFigs:
        case 1:
            while abs(newVal) > 10:
                newVal = newVal/10
                temp_exp += 1
            while abs(newVal) < 1:
                newVal = newVal*10
                temp_exp -= 1
            newVal = round(newVal)
            newVal = newVal * 10**temp_exp
        case 2:
            while abs(newVal) > 100:
                newVal = newVal/10
                temp_exp += 1
            while abs(newVal) < 10:
                newVal = newVal*10
                temp_exp -= 1
            newVal = round(newVal)
            newVal = newVal * 10**temp_exp
        case 3:
            while abs(newVal) > 1000:
                newVal = newVal/10
                temp_exp += 1
            while abs(newVal) < 100:
                newVal = newVal*10
                temp_exp -= 1
            newVal = round(newVal)
            newVal = newVal * 10**temp_exp

    tempSigFigs = numSigFigs
    if abs(newVal) < 10:
        numsAfterDecimal = tempSigFigs - 1
    elif abs(newVal) < 100:
        numsAfterDecimal = tempSigFigs - 2
    else:
        numsAfterDecimal = tempSigFigs - 3
    if numsAfterDecimal < 0:
        tempSigFigs = 3
        numsAfterDecimal = 0
            
    if numSigFigs == 0:
        returnVal = str(newVal)
    else:
        returnVal = f"{newVal:>{tempSigFigs}.{numsAfterDecimal}f}"

    if abs(exponent) > 24:
        if numSigFigs == 0:
            returnVal = f"{inputValue:e}"
        else:
            returnVal = f"{inputValue:>.{tempSigFigs-1}e}"
    
    match exponent:
        case 24:
            returnVal += ' Y'
        case 21:
            returnVal += ' Z'
        case 18:
            returnVal += ' E'
        case 15:
            returnVal += ' P'
        case 12: 
            returnVal += ' T'
        case 9: 
            returnVal += ' G'
        case 6: 
            returnVal += ' M'
        case 3:
            returnVal += ' k'
        case -3:
            returnVal += ' m'
        case -6:
            if encoding.upper() == "UTF-8":
                returnVal += " \u03BC"
            else:
                returnVal += ' u'
        case -9:
            returnVal += ' n'
        case -12:
            returnVal += ' p'
        case -15:
            returnVal += ' f'
        case -18:
            returnVal += ' a'
        case -21:
            returnVal += ' z'
        case -24:
            returnVal += ' y'
        case _:
            returnVal += '  '
            
    return returnVal
    
    
    
def eng_to_float(inputStr: str) -> float:
    """
    Converts string in engineering notation to a float.
    Handles prefixed from 'y-' [10^-24] to 'Y-' [10^24].
    This function can also handle scientific notation inputs.
    NOTE: Exclude the unit from the string. Including the unit will raise a ValueError exception.
    
    EXAMPLE:
        VALID:      '10 k', '3.14', '-412u', or '9.5e-25'.
        INVALID:    '10 kV', '3.14c', 'Hello', or '6.3uu'.
        
    Args:
        inputStr:   (String) The string in engineering notation to convert to a float.
    
    Returns:
        Float representation of converted number.
    """
    
    try:
        returnNum = float(inputStr)
        return returnNum
    except:
        pass
    
    numStr = ""
    prefixStr = ""
    for char in inputStr:
        if char.isdigit() or char in['.', '-', '\u221E']:
            numStr += char
        if char.isalpha():
            prefixStr += char
    
    if numStr == "\u221E":
        return float('inf')
    elif numStr == "-\u221E":
        return float('-inf')
    
    match prefixStr:
        case 'Y':
            exponent = 24
        case 'Z':
            exponent = 21
        case 'E':
            exponent = 18
        case 'P':
            exponent = 15
        case 'T': 
            exponent = 12
        case 'G': 
            exponent = 9
        case 'M': 
            exponent = 6
        case 'k':
            exponent = 3
        case '':
            exponent = 0
        case 'm':
            exponent = -3
        case 'u':
            exponent = -6
        case '\u03BC':
            exponent = -6
        case 'n':
            exponent = -9
        case 'p':
            exponent = -12
        case 'f':
            exponent = -15
        case 'a':
            exponent = -18
        case 'z':
            exponent = -21
        case 'y':
            exponent = -24
        case _:
            raise ValueError(f"'{prefixStr}' is an invalid engineering notation prefix. "
                             "Prefix must be between 10^-24 (y-) and 10^24 (Y-).")
        
    returnNum = float(f"{numStr}e{exponent}")
    return returnNum



def save_to_textfile(valueDict, seriesDict: dict=None, relationships: list=None, header: str=None, footer: str=None) -> str:
    """
    Writes results of e_val_select() to a text file. Name of text file is generated based on UNIX timestamp.
    Encoding will always be in UTF-8.

    Args:
        valueDict (dict):       Returned dictionary from e_val_select()
        seriesDict (dict):      (Optional) Dictionary with component names as keys and selected E-Series as values
        relationships (list):   (Optional) List of component relationships, as strings
        header (str):           (Optional) Line of text to print at beginning of text file
        footer (str):           (Optional) Line of text to print at end of text file
    
    Returns:
        Name of text file, as str.
    """
    timeInt = int(time())
    humanTime = ctime()

    fileName = f"e_series_values_{timeInt}.txt"
    file = open(fileName, 'w', encoding="utf-8")

    file.write("┌───────────────────────────────────────────────────┐\n"
               "│ E - S E R I E S   C O M P O N E N T   V A L U E S │\n"
               "└───────────────────────────────────────────────────┘\n\n")

    if header:
        file.write(f"\n{header}\n\n")
    
    file.write("\nR E S U L T S :\n\n")
    for component in valueDict:
        if seriesDict and component in seriesDict:
            if seriesDict[component] in [3, 6, 12, 24]:
                sigfigs = 2
            else:
                sigfigs = 3
        else:
            sigfigs = 3
        file.write(f"{component}: {eng_note(valueDict[component][0], sigfigs, encoding='UTF-8')}\t\t"
                   f"Error: {valueDict[component][1]*100:.3f}%\n")

    if seriesDict:
        file.write("\n\n__________________________________________________\n\n")
        file.write("E - S E R I E S   S E L E C T I O N :\n\n")
        for component in seriesDict:
            file.write(f"{component}: \t{seriesDict[component]}\n")

    if relationships:
        file.write("\n\n__________________________________________________\n\n")
        file.write("R E L A T I O N S H I P S :\n\n\n")
        for relationship in relationships:
            file.write(f"Relationship:  {relationship}\n\n\n")
            left, right = relationship.split('=')
            left_ex = sp.parse_expr(left)
            right_ex = sp.parse_expr(right)
            file.write(sp.pretty(sp.Eq(left_ex, right_ex), use_unicode=True))
            if not relationships.index(relationship) == len(relationships)-1:
                file.write("\n\n\n\n- - - - - - - - - - - - - - - - - - - - ")
            file.write("\n\n\n")
    file.write("\n__________________________________________________\n")
    file.write(f"\nCalculated on {humanTime}\n")
    if footer:
        file.write(f"{footer}\n")
    file.close()
    return fileName





#################################   VALUE CHECKING   #################################
"""
These functions can be used to check the validity of an input value before it is formatted
for input into e_val_select().

The solving engine does not call these functions. They can be called to validate user input
before calling e_val_select().
"""

class InvalidValueError(Exception):
    """
    Exception for use by component_check, relationship_check, e_series_selection_check, and decade_check.
    This ensures that these cases can be handled seperately from other exceptions, to improve clarity.    
    """

def component_check(component: str, out: str="exception") -> str:
    """
    Checks if a component name follows form expected for SymPy.
    A component name must start with a letter, and can only contain letters, numbers, and underscores.

    Args:
        component (str):    Component name to check
        out (str):         Output out.
                            out="exception": Raises InvalidValueError exception with descriptive error message.
                            out="str":       Only returns string, and does not raise exceptions.
                            Default: "exception"
    
    Returns:
        If out="str", will return text with descriptive error message if the component name is invalid.
        If the component name is valid, an empty string will be returned.
        If an invalid string is entered for "out", then the str "NONE SELECTED" will return.
    """
    errorStr = ""
    if not component[0].isalpha():
        errorStr = "First character is not a letter."
    elif not component.isidentifier():
        errorStr = "Contains characters other than letters, numbers, or underscore."
    elif component in ['pi','e', 'phi', 'sqrt_2','sqrt_3','Y', 'Z', 'E', 'P', 'T', 
                       'G', 'M', 'k', 'm', 'u', 'n', 'p', 'f', 'a', 'z', 'y' ]:
        errorStr = "Component name cannot be reserved keyword."
    
    match out.lower():
        case "exception":
            if errorStr:
                raise InvalidValueError(errorStr)
        case "str":
            return errorStr
        case _:
            return "NONE SELECTED"

def relationship_check(relationship: str, out: str="exception") -> str:
    """
    Checks if a relationship equation follows form expected by the e_val_select() engine.
    It will not check for all possible SymPy syntax issues, but rather guards against common syntax mistakes.

    Args:
        relationship (str): Relationship equation to check
        out (str):         Output out.
                            out="exception": Raises InvalidValueError exception with descriptive error message.
                            out="str":       Only returns string, and does not raise exceptions.
                            Default: "exception"
    
    Returns:
        If out="str", will return text with descriptive error message if the relationship is invalid.
        If the component name is valid, an empty string will be returned.
        If an invalid string is entered for "out", then the str "NONE SELECTED" will return.
    """
    errorStr = ""
    if not '=' in relationship:
        errorStr = "Relationship equation must contain an equals sign."
    if '^' in relationship:
        errorStr = "Caret cannot be used for exponentiation. Use two asterisks (A**B)."
    
    match out.lower():
        case "exception":
            if errorStr:
                raise InvalidValueError(errorStr)
        case "str":
            return errorStr
        case _:
            return "NONE SELECTED"
        

def e_series_selection_check(e_series_selection: int, out: str="exception") -> str:
    """
    Checks if an integer is a valid E-Series number.

    Args:
        e_series_selection (int):   E-Series number to check
        out (str):                 Output out.
                                    out="exception": Raises InvalidValueError exception with descriptive error message.
                                    out="str":       Only returns string, and does not raise exceptions.
                                    Default: "exception"
    
    Returns:
        If out="str", will return text with descriptive error message if the E-Series value is invalid.
        If the component name is valid, an empty string will be returned.
        If an invalid string is entered for "out", then the str "NONE SELECTED" will return.
    """
    errorStr = ""
    if e_series_selection not in [3, 6, 12, 24, 48, 96, 192]:
        errorStr = "Value must be a valid E-Series number."
    
    match out.lower():
        case "exception":
            if errorStr:
                raise InvalidValueError(errorStr)
        case "str":
            return errorStr
        case _:
            return "NONE SELECTED"

def decade_check(decade: float, out: str="exception") -> str:
    """
    Checks if a float is a valid power-of-ten decade.

    Args:
        decade (float): Value to check.
        out (str):     Output out.
                        out="exception": Raises InvalidValueError exception with descriptive error message.
                        out="str":       Only returns string, and does not raise exceptions.
                        Default: "exception"
    
    Returns:
        If out="str", will return text with descriptive error message if the decade is invalid.
        If the component name is valid, an empty string will be returned.
        If an invalid string is entered for "out", then the str "NONE SELECTED" will return.
    """
    errorStr = ""
    decade = eng_to_float(decade)

    if decade == 0:
        errorStr = "Decade cannot be zero."
    elif decade < 0:
        errorStr = "Decade cannot be negative."
    elif not log10(decade).is_integer():
        errorStr = "Value must be a decade expressed a power of 10."
    
    match out.lower():
        case "exception":
            if errorStr:
                raise InvalidValueError(errorStr)
        case "str":
            return errorStr
        case _:
            return "NONE SELECTED"





#################################   PROGRAM SCRIPT   #################################
"""
This part only runs if the program is run as a script.

No part of this section is callable from another file.
"""

if __name__ == "__main__":
    import threading, itertools, collections
    alertTime = 3.0    # Amount of elapsed seconds after which the user will be alerted after e_val_select() function call

    while True: ##### MAIN PROGRAM LOOP
        print("\033[2J\033[H\033[1m\033[1;32;40mE-SERIES COMPONENT SOLVER\n"
              "Determine E-series values for components based on mathematical relationships.\n"
              "Enter \033[0m'EXIT'\033[1;32;40m at any time to exit.\n")
        
        print("\033[1;32;40mPlease enter names of components, one at a time:\n"
              "(Press [ENTER] without input when all components have been entered.\n"
              "At least one component must be entered before continuing.)\033[0m")
        
        comp_str = ""
        while True: ### Component name entry
            try:
                component = input("\033[2K\033[1;33;40mComponent:  \033[0m")
                if component.upper() == 'EXIT':
                    sys.exit("User exit at component entry.")
                elif component == "":
                    if comp_str:
                        break
                    else:
                        raise Exception
                component = str(component)
                component_check(component, out="exception")
                comp_str = comp_str + " " + component
            except InvalidValueError as err:
                print(f"\033[2K\033[1;31;40m{err}\033[0m\033[2F")
            except Exception:
                print("\033[2K\033[1;31;40mInvalid input.\033[0m\033[2F")
        print("\033[1F\033[2K\033[1E\033[2K")
        comp_str = comp_str[1:]
        
        print("\033[1;32;40mPlease enter mathematical relationships for components, one at a time:\n"
              "(Press [ENTER] without input when all relationships have been entered.\n"
              "At least one relationship must be entered before continuing.)\033[0m")
        
        relationship_list = []
        while True: ### Relationship equation entry
            try:
                relationship = input("\033[2K\033[1;33;40mRelationship: \033[0m")
                if relationship.upper() == 'EXIT':
                    sys.exit("User exit at relationship entry.")
                elif relationship == '':
                    if relationship_list:
                        break
                    else:
                        raise Exception
                else:
                    relationship_check(relationship, out="exception")
                    left, right = relationship.split('=')
                    sp.parse_expr(left)
                    sp.parse_expr(right)
                    relationship_list.append(relationship)
            except InvalidValueError as err:
                print(f"\033[2K\033[1;31;40m{err}\033[0m\033[2F")
            except Exception:
                print("\033[2K\033[1;31;40mInvalid input.\033[0m\033[2F")
        print("\033[1F\033[2K\033[1E\033[2K")
        
        print("\033[1;32;40mPlease enter the E-series for each component value:\n"
              "(Valid E-series are: 3, 6, 12, 24, 48, 96, 192)\033[0m")
        
        e_ser_tup = ()
        e_ser_dict = {}
        for comp in comp_str.split(" "):    ### E-Series selection, per component
            if comp:
                while True:
                    try:
                        e_ser = input(f"\033[2K\033[1;33;40mE-Series for {comp}: \033[0m")
                        if e_ser.upper() == 'EXIT':
                            sys.exit("User exit at E-series selection.")
                        e_ser = int(e_ser)
                        e_series_selection_check(e_ser, out="exception")
                        e_ser_tup = e_ser_tup + (e_ser, )
                        e_ser_dict[comp] = e_ser
                        break
                    except InvalidValueError as err:
                        print(f"\033[2K\033[1;31;40m{err}\033[0m\033[2F")
                    except Exception:
                        print("\033[2K\033[1;31;40mInvalid input.\033[0m\033[2F")
        print()
        print("\033[1F\033[2K\n")
        
        print("\033[1;32;40mPlease enter the preferred decade for each component:\n"
              "(Must be entered as a power of 10, and engineering notation can be used.\n"
              "NOTE: Not all components will fall within preferred decade.)\033[0m")
        decade_tup = ()
        for comp in comp_str.split(" "):    ### Decade selection, per component
            if comp:
                while True:
                    try:
                        decade = input(f"\033[2K\033[1;33;40mDecade for {comp}: \033[0m")
                        if decade.upper() == 'EXIT':
                            sys.exit("User exit at decade entry.")
                        decade = eng_to_float(decade)
                        decade_check(decade, out="exception")
                        decade_tup = decade_tup + (decade, )
                        break
                    except InvalidValueError as err:
                        print(f"\033[2K\033[1;31;40m{err}\033[0m\033[2F")
                    except Exception:
                        print("\033[2K\033[1;31;40mInvalid input.\033[0m\033[2F")
        print("\033[2K\n")
        print("\n\n\033[?25l") 

        encoding=sys.getdefaultencoding()
        if encoding == "utf-8":
            waitStr = "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582"
            frameNum = 14
            step = (5, 10)
        else:
            waitStr = '=====   '
            frameNum = 8
            step = (2, 3)
        waitDone = threading.Event()
        waitAnimation = threading.Thread(
        target=lambda: collections.deque(
            (
                (
                print(f"\r\033[2K\033[1;36;40m{waitStr[i%frameNum]}{waitStr[(i+step[0])%frameNum]}{waitStr[(i+step[1])%frameNum]}\033[0m Calculating ...", end="", flush=True),
                sleep(0.1)
                )
            for i in itertools.takewhile(lambda _: not waitDone.is_set(), itertools.count())
            ), 
            maxlen=0),
            daemon=True
        )

        time1 = time() #Used to calculate calculation elapsed time
        try:
            waitAnimation.start()
            values = e_val_select(comp_str, relationship_list, e_ser_tup, decade_tup) # Engine call
            waitDone.set()
            waitAnimation.join()
        except ValueError as error:
            waitDone.set()
            waitAnimation.join()
            time2 = time()
            if (time2 - time1) > alertTime:
                print("\a", end="", flush=True)    # Terminal bell
            print(f"\r\033[2K\033[1;31;40m{error}\033[0m\033[?25h")
            print("\n\n")
            while True:
                print("\033[2F\033[2K\033[1;33;40m[Enter [R] to re-run with new values, "
                          "or press [ENTER] to quit.]\033[0m\033[1E\033[?25h")
                option = input("\033[2K").upper()
                if option == 'R':
                    break
                elif option == '':
                    sys.exit("User exit at value error.")
                else:
                    print(f"\033[2F\033[2K\033[1;31;40mInvalid command.")
            continue    # Skip rest of script and restart from top of main loop.

        except KeyboardInterrupt:
            print("\r\033[2K\033[?25h\033[0m")
            sys.exit("User keyboard interrupt.")

        except Exception as error:
            waitDone.set()
            waitAnimation.join()
            time2 = time()
            if (time2 - time1) > alertTime:
                print("\a", end="", flush=True)    # Terminal bell
            print("\r\033[2K\033[?25h\033[0m")
            sys.exit(error)

        time2 = time()
        elapsed = round(time2 - time1, 3)
        if elapsed > alertTime:
            print("\a", end="", flush=True)
        if elapsed == 1.0:
            computed_time = f"{elapsed} second."
        elif elapsed < 0.001:
            computed_time = "less than one millisecond."
        else:
            computed_time = f"{elapsed} seconds."
        print(f"\r\033[2KComputed in {computed_time}\n\n")
        
        print_e_val_results(values, e_ser_dict)

        print("\n\n\n\n")
        allowSave = True
        while True: ### End option selection
            if allowSave:
                print("\033[2F\033[2K\033[1;33;40m[Enter [S] to save to textfile or [R] to re-run with new values, "
                      "otherwise press [ENTER] to quit.]\033[0m\033[1E\033[?25h")
            else:
                print("\033[2F\033[2K\033[1;33;40m[Enter [R] to re-run with new values, "
                      "or press [ENTER] to quit.]\033[0m\033[1E\033[?25h")
            
            option = input("\033[2K").upper()
            if option == 'S' and allowSave:
                allowSave = False
                name = save_to_textfile(values, e_ser_dict, relationship_list, footer=f"Computed in {computed_time}")
                print(f"\033[2F\033[2K\033[1;33;40mSaved to \033[0m{name}")
            elif option == 'R':
                break
            elif option == '':
                print("\033[0m\n\n")
                sys.exit("User exit at completion.")
            else:
                print(f"\033[2F\033[2K\033[1;31;40mInvalid command.")
