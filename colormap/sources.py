from cantrips.watch.expression import IdentityExpression


_ = IdentityExpression()  # given the scope, this will return itself
rgb = _.rgb  # given the scope, this will return its rgb member
hsv = _.hsv  # given the scope, this will return its hsv member
luv = _.luv  # given the scope, this will return its luv member
lab = _.lab  # given the scope, this will return its lab member
hed = _.hed  # given the scope, this will return its hed member
xyz = _.xyz  # given the scope, this will return its xyz member
