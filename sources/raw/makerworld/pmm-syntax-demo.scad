// We will demonstrate most of the syntax supported by Parametric Model Maker here.
// This file is NOT to demonstrate the syntax of OpenSCAD. 
// Please refer to the official documentation for more details:
// https://en.wikibooks.org/wiki/OpenSCAD_User_Manual

////////////////////////////////////////
// INTRODUCTION
////////////////////////////////////////

// Use /* [name] */ to create a new tab.
// This can be used to organize your parameters into a different tab.
/* [Parameters] */

// For each parameter, you can use the following syntax:

NoDesc = 1;

// You can also add a description to each parameter by adding a comment before the parameter.

// The comment will be displayed as the description of the parameter.
WithDesc = 1;

// In the following parts, we will demonstrate different types of parameters.

////////////////////////////////////////
// DROPDOWN
////////////////////////////////////////
/* [Dropdown] */
// To define a dropdown box, you can use the following syntax:
// parameterName = value; // [value1, value2, value3]

// Dropbox for numbers
NumberDropdown = 2; // [0, 1, 2, 3]

// Dropbox for string
StringDropdown = "foo"; // [foo, bar, baz]


// You can also add a label to each value with the following syntax,
// so that the dropdown box will display the label instead of the value:
// parameterName = value; // [value1:label1, value2:label2, value3:label3]

// Labeled dropdown box for numbers
Labeled_values = 10; // [10:L, 20:M, 30:XL]

// Labeled dropdown box for strings
Labeled_value = "S"; // [S:Small, M:Medium, L:Large]


////////////////////////////////////////
// SLIDER
////////////////////////////////////////
/*[ Slider ]*/

// To define a slider, you can use the following syntax:
// parameterName = value; // [min:max]
// You can also add a step size to the slider with the following syntax:
// parameterName = value; // [min:step:max]

// Slider with min and max
slider = 34; // [10:100]

// Step slider with min, max and step
stepSlider = 2; //[0:5:100]

// Step slider for decimal numbers
decimalSlider = 2; //[0:0.1:100]

////////////////////////////////////////
// CHECKBOX
////////////////////////////////////////
/* [Checkbox] */
// To define a checkbox, you can use the following syntax(value is true or false):
// parameterName = value;

// Checkbox for boolean
checkbox1 = true;


////////////////////////////////////////
// SPINBOX
////////////////////////////////////////
/* [Spinbox] */
// To define a spinbox, you can use the following syntax(value is a number):
// parameterName = value;

// Spinbox with step size 1
SpinboxForInt = 5;
// Spinbox with step size 0.1
SpinboxForDecimal = 5.0;


////////////////////////////////////////
// TEXTBOX
////////////////////////////////////////
/* [Textbox] */
// To define a textbox, you can use the following syntax(value is a string):
// parameterName = value;

// Text box for string
stringTextbox = "hello";

////////////////////////////////////////
// VECTOR
////////////////////////////////////////
/* [Vector] */
// We can define a vector of numbers. Users can adjust each value with a spinbox.
// You can use the following syntax(value is a number):
// parameterName = [value1, value2, value3];

// Vector with single value
VectorSingleValue = [1];
// Vector with multiple values
VectorMultipleValues = [12, 34, 46, 24];

// You can also define the range and step size with the following syntax:
// parameterName = [value1, value2, value3]; // [min:step:max]

// Vector with range and step size
VectorRGB = [128, 23, 231]; //[0:1:255]

// Vector with step size 0.1
VectorWithStep = [ 12, 34 ]; //[:0.1:]

////////////////////////////////////////
// FILE
////////////////////////////////////////
/* [File] */
// Parametric Model Maker allows users to upload PNG, SVG and STL.

// Ask for a PNG file. The value has to be "default.png".
filenamePNG1 = "default.png";
// You can ask for multiple files with the same type
filenamePNG2 = "default.png";

// Ask for a SVG file. The value has to be "default.svg".
filenameSVG = "default.svg";

// Ask for a STL file. The value has to be "default.stl".
filenameSTL = "default.stl";

////////////////////////////////////////
// COLOR
////////////////////////////////////////
/* [Color] */
// Parametric Model Maker can generate multi-color models.
// Users can choose a color with a color picker with the following syntax(value
// has to be a color in hex format):
// parameterName = "#000000"; //color

color = "#FF0000"; // color


////////////////////////////////////////
// FONT
////////////////////////////////////////
/* [Font] */
// Parametric Model Maker integrates most of google fonts.
// Parametric Model Maker also provides a font selector for users to choose a font.
// Users can choose a font with the following syntax:
// parameterName = "Arial"; //font

font = "HarmonyOS Sans SC:style=Black"; //font

// If you want to hide some parameters, you can use the hidden tag.
/* [Hidden] */
hiddenParam = false;

////////////////////////////////////////
// MULTI-PLATE
////////////////////////////////////////
// NOTES: By using this feature, users CANNOT download the STL file. It is
// recommended to provide two versions of SCAD files.

// Parametric Model Maker supports generating multi-plate models.
// To do so, you should define specific modules for each plate.
// The name of module should be in syntax: mw_plate_1(), mw_plate_2(), etc.
module mw_plate_1() {
    color("#FF0000") cube([10, 10, 10]);
}

module mw_plate_2() {
    color("#00FF00") cube([10, 10, 10]);
}

// It is allowed that one of the plates generates empty models.
// You can use this feature to make your code more adaptive. For example, if
// your model contains several parts, you can separate them into different
// plates only when they cannot fit into one plate.
module mw_plate_3() {
    // empty
}

// You can also define a specific module for users to preview the assembly view.
module mw_assembly_view() {
    mw_plate_1();
    translate([0, 0, 10]) mw_plate_2();
}
