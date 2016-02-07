import collections
from numpy import ones, zeros
from .spaces import rgb, ColorSpace, RGB
from cantrips.watch.expression import Expression
from cantrips.watch.scope import Scope


class MappingContext(collections.namedtuple('_MappingContext', ('image', 'cache'))):
    """
    A mapping context relates to an execution of a Map's run() method.
    Involved the following:

    - Referencing the current image.
    - Referencing the current run-wide colorspace.
    - Can calculate and cache elements.

    Even if it is not allowed to cache, will store the last processing result.

    Another use is in a masked-chunk level. In this case, the initial rgb image
      is not the full one, but just a chunk determined by a formerly-existent
      mask. The usage, however, is the same.
    """

    def __new__(cls, image, cache):
        value = super(MappingContext, cls).__new__(cls, image, {} if cache else None)
        value.__colorspace = rgb
        value._set_last(None, None)
        return value

    def _set_last(self, space, image):
        self.__last_image = image
        self.__last_space = space
        return image

    @property
    def colorspace(self):
        return self.__colorspace

    @colorspace.setter
    def colorspace(self, value):
        if value:
            self.__colorspace = value

    def process_image(self, colorspace):
        """
        Processes (and caches, if applicable) the image.

        If the requested format is rgb we return the initial image.
        If the requested format is the same last format, we return the same last image.
        Otherwise we compute it or recover it from cache, according to the case.
        """

        if not isinstance(rgb, ColorSpace):
            raise TypeError("process_image() expects a single parameter of type ColorSpace")

        if colorspace == rgb:
            return RGB(self.image)

        if colorspace == self.__last_space:
            return self.__last_image

        if self.cache is None:
            return self._set_last(colorspace, colorspace.encoder(self.image))
        else:
            if colorspace not in self.cache:
                self.cache[colorspace] = self._set_last(colorspace, colorspace.encoder(self.image))
            return self.cache[colorspace]


class Masker(collections.namedtuple('Masker', ('masker', 'colorspace'))):
    """
    A masker is a function executed with a colorspace (by default rgb).
    Takes a function, and a colorspace, to process an image in a mapping context.
    """

    def __new__(cls, masker, colorspace=rgb):
        if not isinstance(rgb, ColorSpace):
            raise TypeError("`colorspace` parameter for Masker must be a ColorSpace instance")
        return super(Masker, cls).__new__(cls, masker, colorspace)

    def get_mask(self, context):
        wrapper = context.process_image(self.colorspace)
        if isinstance(self.masker, Expression):
            scope = Scope()
            setattr(scope, self.colorspace.components, wrapper)
            result = scope['$eval'](self.masker)
        else:
            result = self.masker(wrapper)
        return result


class Action(collections.namedtuple('Action', ('action', 'colorspace'))):
    """
    An action executes over a masked image. For the same masked image, successive
      actions will be applied and, in this way, it's a nonsense to cache the results,
      but only take note on the applied colorspace.
    """

    def __new__(cls, action, colorspace=rgb):
        if not isinstance(rgb, ColorSpace):
            raise TypeError("`colorspace` parameter for Action must be a ColorSpace instance")
        return super(Action, cls).__new__(cls, action, colorspace)

    def execute(self, chunk):
        """
        Executes the action, taking the chunk in RGB[A] and returning it in RGB[A] as well but having
          a specific colorspace for processing.
        :param chunk:
        :return:
        """

        # Wrap the input
        if self.colorspace == rgb:
            wrapper = RGB(chunk)
        else:
            wrapper = self.colorspace.encoder(chunk)

        # Process input -> output
        if isinstance(self.action, Expression):
            # Assign the wrapper as scope member with appropriate name.
            scope = Scope()
            setattr(scope, self.colorspace.components, wrapper)
            result = scope['$eval'](self.action)
        else:
            result = self.action(wrapper)

        # Unwrap the output
        if self.colorspace == rgb:
            return result
        else:
            return self.colorspace.decoder(result)


class MappingEntry(collections.namedtuple('MappingEntry', ('masker', 'actions'))):
    """
    A mapping entry is an IF-THEN clause for the mapping process.
    """

    def __new__(cls, masker, colorspace=rgb):
        return super(MappingEntry, cls).__new__(cls, Masker(masker, colorspace), [])

    def do(self, action, colorspace=rgb):
        """
        Adds this action to itself. Returns itself for builder pattern.
        :param action:
        :param colorspace:
        :return:
        """
        self.actions.append(Action(action, colorspace))
        return self


class Mapper(collections.namedtuple('Mapper', ('entries',))):
    """
    Mapper object.
    """

    def __new__(cls):
        return super(Mapper, cls).__new__(cls, [])

    def on(self, masker, colorspace=rgb):
        """
        Adds a mapping entry. Returns it.
        :return:
        """
        entry = MappingEntry(masker, colorspace)
        self.entries.append(entry)
        return entry

    def run(self, image, cache):
        """
        Runs the mapping. Returns the mapped image.
        :param image:
        :param cache:
        :return:
        """

        if len(image.shape) != 3 or image.shape[2] not in (3, 4):
            raise ValueError("Image to be masked must have three dimensions (non-palette colors)")

        context = MappingContext(image, cache)
        # Guess the masks. Keep the remaining mask.
        premasked = []
        initial_mask = ones(image.shape[0:2], dtype=bool)
        for entry in self.entries:
            matched_mask = initial_mask & entry.masker.get_mask(context)
            premasked.append((matched_mask, entry))
            initial_mask = initial_mask & ~matched_mask
        # Apply actions on every mask. Apply a null action on the remaining mask.
        remaining_mask = initial_mask
        new_image = zeros(image.shape[0:3], dtype=image.dtype)
        for mask, entry in premasked:
            new_image[mask] = image[mask]
            for action in entry.actions:
                new_image[mask] = action.execute(new_image[mask])
        new_image[remaining_mask] = image[remaining_mask]
        return new_image