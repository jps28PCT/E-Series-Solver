# E-Series Value Solver
This application automates the process of component value selection in real-world systems.<br/>
<br/>
The program solves systems of component-relationship equations for real-world [E-Series](https://wikipedia.org/wiki/E_series_of_preferred_numbers) values. The systems can be fully-determined or under-determined. Every combination of E-Series values is tested based on selected parameters, and the combination with the smallest error is found.

> [!NOTE]<br/>
> Requires Python 3.11 or later and SymPy 1.14.0 or later.<br/>
> If run without SymPy installed, a warning will be printed and the program will end.<br/>
<br/>

The file `e_series_solver.py` can be run either as a [script](#running-as-a-script), or used as an [API](#using-as-an-api).<br/>

The solver requires component names, component relationships, component E-Series, and desired component decades in order to solve for the best real-world component values. Any number of component names and relationshp equations can be passed, so the solver engine can analyze complex systems.


### Component Names
Component names must start with a letter, and letters and numbers can follow. Names can be of any length. It is recommended to use standard schematic [component reference designators](https://wikipedia.org/wiki/Reference_designator).<br/>
#### Examples:
`'R1'`, `'R2'`, `'C1'`, `'L1'`, etc.


### Component Relationship Equations
These equations should be based on the topology of the circuit, and should reflect the desired effect for the circuit. They can be based on standard circuit equations for known topologies, or they can be found analytically through mesh/nodal circuit analysis. Use standard Python and SymPy algebraic operators. All equations must include an equals sign (`=`). Pre-defined constants are also available. Values can be multiplied by [engineering notation prefixes](https://en.wikipedia.org/wiki/Engineering_notation), from "yotta-" (10<sup>24</sup>) to "yocto-" (10<sup>-24</sup>) [use '`u`' for 'micro'].<br/>
When finished entering component relationships, press `[ENTER]` on the empty input line.

#### Examples:
`" 3.3 = 5 * (R1/(R1+R2)) "`<br/>
`" 1*k = 1 / (2 * pi * sqrt(L1 * C1)) "`<br/>

#### Valid Operators:
| Operator | Use |   | Operator | Use |
| :---: | :---: | :---: | :---: | :---: |
| `+` | addition |   | `**`| exponentiation |
| `-` | subtraction |   | `sqrt(X)` | square root |
| `*` | multiplication |   | `X**(1/n)` | n-th root |
| `/` | division |   | `log(X, n)` | log, base n|

Other SymPy functions, like `sin( )` and `cos( )`, are also usable.

#### Pre-Defined Constants:
| Constant | Symbol | Value |
| :---: | :---: | :--- |
| π | `pi` | 3.14159265358979323846264338327950 |
| e | `e` | 2.71828182845904523536028747135266 |
| ϕ | `phi` | 1.61803398874989484820458683436563 |
| √2 | `sqrt_2` | 1.41421356237309504880168872420969 |
| √3 | `sqrt_3` | 1.73205080756887729352744634150587 |


### Component E-Series
Each component must be associated with an E-Series. Higher E-Series have smaller steps between values, and thus have more values per decade. Each series also has sequentially smaller maximum tolerance. These values must be integers.

#### E-Series Numbers:
`3`, `6`, `12`, `24`, `48`, `96`, `192`


### Decades
Each component must also be associated with a desired decade. Decades can be entered as decimal values, or in scientific or engineering notation. They must be valid powers of 10. Some component values may not fall within their decade, as the final values are dictated by the relationship equations. However, solution sets with more component values within their assigned decades are prioritized while still finding the smallest total system error.

#### Examples:
`1`, `100`, `0.001`, `'10k'`, `'100u'`, `1e17`, `1e-11`, etc.<br/>

<br/>

***
***

## Running as a Script
Running as a script allows the program to be used as a CLI application.<br/>

The application can be installed from the most recent [release](https://github.com/jps28PCT/E-Series-Solver/releases/tag/v1.1.1). Ensure the correct binary is installed for your operating system.

Alternatively, the Python file can be downloaded and run directly. To do so, open the file's directory in a terminal and type the following command:
```bash
$ python e_series_solver.py
```

The program will prompt sequentially for each input. At any time, type `EXIT` to exit.
<br/>

### Inputs
First, [component names](#component-names) are entered.  When finished entering components, press `[ENTER]` on the last empty input line to continue.
```ansi
Component:  R1
Component:  R2
Component:
```
<br/>

Second, [component relationship equations](#component-relationship-equations) are entered. After all relationship equations are entered, press `[ENTER]` on the last empty input line to continue.
```ansi
Relationship: 3.3 = 5 * (R2 / (R1 + R2))
Relationship:
```
<br/>

Next, [E-Series are selected](#component-e-series) for each entered component. Only the number of the series should be entered. The program will proceed once every component has been associated with an E-Series.
```ansi
E-Series for R1: 24
E-Series for R2: 24
```
<br/>

Lastly, the desired [decade](#decades) is selected for each component. The program will proceed once every component has been associated with a decade.
```ansi
Decade for R1: 10k
Decade for R2: 1k
```
<br/>

### Outputs
After all inputs are entered, the calculation will run. Once complete, the results will written to the terminal. Both the determined component values and their percent errors will be displayed.
```ansi
┌───────────────────────────────────────┐
│            R E S U L T S :            │
└───────────────────────────────────────┘
R1: 4.7 k               Error: 0.259%
R2: 9.1 k               Error: 0.000%
```
<br/>

From here, the results can be saved by a text file by typing `S`, or the application can be re-run by typing `R`. The script can be terminated by pressing `[ENTER]` without any input.

#### LC Oscillator Example
The goal is to create an LC tank circuit resonant at 1.5 kHz, using an E-24 inductor and an E-12 capacitor. It is easier to find inductors in hundreds of microhenries, and ceramic capacitors can be cheaply accurate down to nanofarads.

##### LC Oscillator frequency equation:
```math
f= \frac{1}{2\pi \sqrt{LC}}
```

##### Script:
```ansi
E-SERIES COMPONENT SOLVER
Determine E-series values for components based on mathematical relationships.
Enter 'EXIT' at any time to exit.

Please enter names of components, one at a time:
(Press [ENTER] without input when all components have been entered.
At least one component must be entered before continuing.)
Component:  L1
Component:  C1


Please enter mathematical relationships for components, one at a time:
(Press [ENTER] without input when all relationships have been entered.
At least one relationship must be entered before continuing.)
Relationship: 1.5*k = 1 / (2 * pi * sqrt(L1 * C1))


Please enter the E-series for each component value:
(Valid E-series are: 3, 6, 12, 24, 48, 96, 192)
E-Series for L1: 24
E-Series for C1: 12


Please enter the preferred decade for each component:
(Must be entered as a power of 10, and engineering notation can be used.
NOTE: Not all components will fall within preferred decade.)
Decade for L1: 100u
Decade for C1: 10n


Computed in 0.52 seconds.

┌───────────────────────────────────────┐
│            R E S U L T S :            │
└───────────────────────────────────────┘
L1: 750 μ               Error: 0.000%
C1: 15 μ                Error: 0.070%


[Enter [S] to save to textfile or [R] to re-run with new values, otherwise press [ENTER] to quit.]

```
The application selected a 750 µH inductor, and a 15 µF capacitor. Both components have an error less than the maximum tolerance of their selected E-Series.<br/>
<br/>
Plugging these values into the LC resonant frequency equation yields:
```math
\frac{1}{2\pi \sqrt{(750 \mu H) \cdot (15 \mu F)}} \approx 1.50053 kHz
```
This has a percent error of 0.035% from the desired frequency.<br/>

<br/>

***
***

## Using as an API
Custom scripts can be developed to automate workflows using the component value solver engine.<br/>
<br/>
The package can be installed using `pip`.
```bash
pip install e-series-solver
```

To use, import as a library at the top of the file. The file can be imported as the name `ess` for simplicity.

```python
import e_series_solver as ess
```
Now, the custom script has access to all functions. For full function descriptions, view the docstrings within [e_series_solver.py](e_series_solver.py).

#### Functions:
- `e_val_select()` -  Solver engine
- `print_e_val_results()` - ANSI terminal printer for values returned from solver engine
- `save_e_val_results()` - Writes values returned from solver engine to a text file
- `float_to_eng()` - Converts floats to strings in SI engineering notation
- `eng_to_float()` - Converts strings in SI engineering notation to floats
- `component_check()` - Quick input validation for component names
- `relationship_check()` - Quick input validation for component relationship equations
- `e_series_selection_check()` - Quick input validation for E-Series selection
- `decade_check()` - Quick input validation for component decade

<br/>

### Using the Solver Engine
The E-Series solver engine is callable as the function `e_val_select()`. 

```python
e_val_select(components, relationships, e_series_selection, decade_selection)
```


#### Arguments:

- `components` (str) - All [component names](#component-names), separated by spaces.

- `relationships` (list) - List of [component relationship equations](#component-relationship-equations), where equations are expressed as strings.

- `e_series_selection` (tuple) - [E-Series numbers](#component-e-series) associated with each component, in the same order as `components`

- `decade_selection` (tuple) - Desired [component decades](#decades) associated with each component, expressed as floats or strings. Must be in the same order as `components`.
<br/>

#### Returns:
Dictionary with component names as keys, and tuples containing (`E_VALUE`, `ERROR`) as values.
- `E_VALUE` is the calculated E-Series value for the component, as a decimal float.
- `ERROR` is the raw decimal percent error between the calculated E-Series value and the ideal value, as a decimal float.
<br/>

#### Raises:
`ValueError` if a negative or zero component value is calculated.<br/>
This indicates the relationship equations are unsolvable for real-world component values.

<br/>

#### Example of Using the Solver Engine
```python
import e_series_solver as ess

# Create voltage divider from 5V to 3.3V
# with total current draw of 10mA

components = "R1 R2"
relationships = [ "3.3 = 5 * R2/(R1+R2)",  "5 / (R1+R2) = 10*m"]       
e_series_selection = (24, 24)
decade_selection = (100, '1k')

results = ess.e_val_select(components, relationships, e_series_selection, decade_selection)
print(results)
```

#### Output:
```bash
{'R1': (160.0, 0.058823529411764705), 'R2': (330.0, 0.0)}
```
> R1 = 160 Ω, with 5.882% error<br/>
> R2 = 330 Ω, with 0% error

<br/>

### Custom Scripts
When running through multiple iterations of similar topologies, repeatedly entering component names and equations may become tedious. Writing a script allows more control over the environment, and thus a custom workflow can be developed.

Further equation formatting can become more intuitive by using f-strings. Lengthy or repeated expressions can be assigned to a variable, and an f-string can substitute the variable into equation strings.

<br/>

#### Sallen-Key Low-Pass Filter Example
Sallen-Key filters are well-studied topologies, and have [defined equations](https://www.ti.com/lit/an/sloa024b/sloa024b.pdf). Here, the filters will also have a negative-feedback, non-inverting gain stage.

##### Cutoff frequency:
```math
f_{c} = \frac{1}{2\pi\sqrt{R_1R_2C_1C_2}}
```

##### Voltage gain:
```math
A_v = 1 +\frac{R_f}{R_g}
```

##### Quality factor:
```math
Q = \frac{\sqrt{R_1R_2C_1C_2}}{R_1C_1 + R_2C_1 + R_1C_2(1-A_v)}
```
<br/>

##### Custom script:

```python
import e_series_solver as ess

### INPUT VALUES
fc = '20k'          # Cutoff frequency
Q = '1/sqrt_2'      # Filter response (Butterworth)
Av = 2              # Filter gain

### Components
components =        "R1 R2 Rf Rg C1 C2"
e_series_selection = (24, 24, 24, 24, 12, 12)
decade_selection =   ('1k', '1k', '10k', '10k', '1u', '1u')

### Equations
tau = "sqrt(R1*R2*C1*C2)"   # Expression to simplify equations
K = "1 + (Rf/Rg)"           # Non-inverting gain

# cutoff frequency equation
freq = f"{ess.eng_to_float(fc)} = 1 / (2 * pi * ({tau}))"   

# Voltage gain equation
gain = f"{Av} = {K}"            

# Q equation
qual = f"{Q} = ({tau}) / (R1*C1 + R2*C1 + (1-({K}))*R1*C2)"

relationships = [freq, gain, qual]

# Solver engine
results = ess.e_val_select(components, relationships, e_series_selection, decade_selection) 

ess.print_e_val_results(results, e_series_selection) # Prints results to terminal

headerStr = (f"fc = {fc}\n"
             f"Q = {Q}  \n"
             f"Av = {Av}")

ess.save_e_val_results(results, e_series_selection, header=headerStr) # Save to text file

```
##### Output:
```ansi
┌───────────────────────────────────────┐
│            R E S U L T S :            │
└───────────────────────────────────────┘
R1: 1.80 k              Error: 0.000%
R2: 1.10 k              Error: 0.000%
Rf: 10.0 k              Error: 0.000%
Rg: 10.0 k              Error: 0.000%
C1: 6.80 n              Error: 0.000%
C2: 4.70 n              Error: 0.071%
```

##### Saved text file:
```
┌───────────────────────────────────────────────────┐
│ E - S E R I E S   C O M P O N E N T   V A L U E S │
└───────────────────────────────────────────────────┘


fc = 20k
Q = 1/sqrt_2  
Av = 2


R E S U L T S :

R1: 1.80 k		Error: 0.000%
R2: 1.10 k		Error: 0.000%
Rf: 10.0 k		Error: 0.000%
Rg: 10.0 k		Error: 0.000%
C1: 6.80 n		Error: 0.000%
C2: 4.70 n		Error: 0.071%

__________________________________________________

Calculated on Sun Jul 19 21:53:01 2026
```
