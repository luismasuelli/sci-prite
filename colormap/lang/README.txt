A mapping script can have the following structure:

alpha require;
require '/path/to/my/file.py' as my_plugin; # relative to source file
for $index, $my_hue in [0:360:30] do
  target '/path/to/target/%.png' with [$index]; # relative to input file
  on hsv pixels: h == 0 do
    # scalar assignment
    h = $my_hue / 360.;

    # "range map" assignment (combines + and *). supports saturation. supports modulo rotation.
    h = 0 .. .25 to .25 .. .75;

    # "add by" assignment. supports saturation (e.g. (|s|) +=). supports modulo rotation (e.g. ~|s|~ +=).
    s += .3;

    # "multiply by" assignment. supports saturation and modulo rotation.
    v *= .5;
  end;
  on ... ... do
    ...
  end
end

===============================================================================

Directives:

1. Alpha:

   Rules:
     $ = alpha (include|discard) semicolon ;

   Tokens:
     alpha, include, discard: keywords
     semicolon: ,

   Semantic:
     The expected image will be loaded with RGB or with RGBA

2. Require plugin:

   Rules:
     $ = require string as name semicolon ;

   Tokens:
     require, as: keywords
     semicolon: ,
     string, name: values by regex

   Semantic:
     Requires a python file to use its functions

3. For loop:

   Rules:
     $ = for variable, variable in (range|vector) ;

   Tokens:
     for, in: keywords
     variable: values by regex

   Semantic:
     Iterates the content inside

4. do .. end:

   Tokens:
     do, end: keywords

   Semantic:
     Block delimitation

5. Target image file:

   Rules:
     $ = target string formatter semicolon ;
     formatter = with vector | ;

   Tokens:
     target, with: keywords
     string: value by regex
     semicolon: ,

   Semantic:
     Specifies the image output file, either absolute or
       relative to the input image.

6. Mappings:

   Rules:
     $ = mapping_scslist ;
     mapping_scslist = mapping | mapping semicolons mapping_scslist ;
     mapping = on space pixels colon condition do actions_scslist end ;
     space = rgb | hed | hsv | luv | lab | xyz | ;
     actions_scslist = action | action semicolons actions_scslist ;
     semicolons = semicolon semicolons | ;

   Tokens:
     on, rgb, hed, hsv, luv, lab, xyz, pixels: keywords
     semicolon: ;
     colon: :

   Semantic:
     Defines a mapping rule and actions.

7. Condition

8. Action

*. Additional elements:

   Vector:

     Rules:
       $ = [ numbers ] ;
       numbers = number_cslist | ;
       number_cslist = number_expression | number , number_cslist ;
       number_expression = an expression involving only $variables and numbers ;

     Tokens:
       [ ] ,

     Semantic:
       Numeric vector object

   Range:

     Rules:
       $ = [ slice ] ;
       slice = opt_number colon opt_number colon opt_number ;
       opt_number = number_expression | ;
       number_expression = an expression involving only $variables and numbers ;

     Tokens:
       [ ]
       colon: :

     Semantic:
       Range vector object (as provided by range())