r"""Mobjects representing text rendered using LaTeX.

.. note::
   Just as you can use :class:`~.Text` (from the module :mod:`~.text_mobject`) to add text to your videos, you can use :class:`~.Tex` and :class:`~.MathTex` to insert LaTeX.

The Tex mobject
+++++++++++++++

.. manim:: HelloLaTeX
    :save_last_frame:

    class HelloLaTeX(Scene):
        def construct(self):
            tex = Tex(r'\LaTeX').scale(3)
            self.add(tex)

Note that we are using a raw string (``r'---'``) instead of a regular string (``'---'``).
This is because TeX code uses a lot of special characters - like ``\`` for example -
that have special meaning within a regular python string. An alternative would have
been to write ``\\`` as in ``Tex('\\LaTeX')``.

The MathTex mobject
+++++++++++++++++++
Anything enclosed in ``$`` signs is interpreted as maths-mode:

.. manim:: HelloTex
    :save_last_frame:

    class HelloTex(Scene):
        def construct(self):
            tex = Tex(r'$\xrightarrow{x^2y^3}$ \LaTeX').scale(3)
            self.add(tex)

Whereas in a :class:`~.MathTex` mobject everything is math-mode by default.

.. manim:: MovingBraces

    class MovingBraces(Scene):
        def construct(self):
            text=MathTex(
                "\\frac{d}{dx}f(x)g(x)=",       #0
                "f(x)\\frac{d}{dx}g(x)",        #1
                "+",                            #2
                "g(x)\\frac{d}{dx}f(x)"         #3
            )
            self.play(Write(text))
            brace1 = Brace(text[1], UP, buff=SMALL_BUFF)
            brace2 = Brace(text[3], UP, buff=SMALL_BUFF)
            t1 = brace1.get_text("$g'f$")
            t2 = brace2.get_text("$f'g$")
            self.play(
                GrowFromCenter(brace1),
                FadeIn(t1),
                )
            self.wait()
            self.play(
                ReplacementTransform(brace1,brace2),
                ReplacementTransform(t1,t2)
                )
            self.wait()


LaTeX commands and keyword arguments
++++++++++++++++++++++++++++++++++++
We can use any standard LaTeX commands in the AMS maths packages. For example the ``mathtt`` math-text type, or the ``looparrowright`` arrow.

.. manim:: AMSLaTeX
    :save_last_frame:

    class AMSLaTeX(Scene):
        def construct(self):
            tex = Tex(r'$\mathtt{H} \looparrowright$ \LaTeX').scale(3)
            self.add(tex)

On the manim side, the :class:`~.Tex` class also accepts attributes to change the appearance of the output.
This is very similar to the :class:`~.Text` class. For example, the ``color`` keyword changes the color of the TeX mobject:

.. manim:: LaTeXAttributes
    :save_last_frame:

    class LaTeXAttributes(Scene):
        def construct(self):
            tex = Tex(r'Hello \LaTeX', color=BLUE).scale(3)
            self.add(tex)

Extra LaTeX Packages
++++++++++++++++++++
Some commands require special packages to be loaded into the TeX template. For example,
to use the ``mathscr`` script, we need to add the ``mathrsfs`` package. Since this package isn't loaded
into manim's tex template by default, we add it manually:

.. manim:: AddPackageLatex
    :save_last_frame:

    class AddPackageLatex(Scene):
        def construct(self):
            myTemplate = TexTemplate()
            myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
            tex = Tex(r'$\mathscr{H} \rightarrow \mathbb{H}$}', tex_template=myTemplate).scale(3)
            self.add(tex)

Substrings and parts
++++++++++++++++++++
The TeX mobject can accept multiple strings as arguments. Afterwards you can refer to the individual
parts either by their index (like ``tex[1]``), or you can look them up by (parts of) the tex code like
in this example where we set the color of the ``\bigstar`` using :func:`~.set_color_by_tex`:

.. manim:: LaTeXSubstrings
    :save_last_frame:

    class LaTeXSubstrings(Scene):
        def construct(self):
            tex = Tex('Hello', r'$\bigstar$', r'\LaTeX').scale(3)
            tex.set_color_by_tex('igsta', RED)
            self.add(tex)

Note that :func:`~.set_color_by_tex` colors the entire substring containing the Tex searched for,
not just the specific symbol or Tex expression searched for. Consider the following example:

.. manim:: IncorrectLaTeXSubstringColoring
    :save_last_frame:

    class IncorrectLaTeXSubstringColoring(Scene):
        def construct(self):
            equation = MathTex(
                r"e^x = x^0 + x^1 + \frac{1}{2} x^2 + \frac{1}{6} x^3 + \cdots + \frac{1}{n!} x^n + \cdots"
            )
            equation.set_color_by_tex("x", YELLOW)
            self.add(equation)

As you can see, this colors the entire equation yellow, contrary to what may be expected. To color only ``x`` yellow, we have to do the following:

.. manim:: CorrectLaTeXSubstringColoring
    :save_last_frame:

    class CorrectLaTeXSubstringColoring(Scene):
        def construct(self):
            equation = MathTex(
                r"e^x = x^0 + x^1 + \frac{1}{2} x^2 + \frac{1}{6} x^3 + \cdots + \frac{1}{n!} x^n + \cdots",
                substrings_to_isolate="x"
            )
            equation.set_color_by_tex("x", YELLOW)
            self.add(equation)

By setting ``substring_to_isolate`` to ``x``, we split up the :class:`~.MathTex` into substrings
automatically and isolate ``x`` components into individual substrings. Only then can :meth:`~.set_color_by_tex` be used to achieve the desired result.

LaTeX Maths Fonts - The Template Library
++++++++++++++++++++++++++++++++++++++++
Changing fonts in LaTeX when typesetting mathematical formulae is a little bit more tricky than
with regular text. It requires changing the template that is used to compile the tex code.
Manim comes with a collection of :class:`~.TexFontTemplates` ready for you to use. These templates will all work
in maths mode:

.. manim:: LaTeXMathFonts
    :save_last_frame:

    class LaTeXMathFonts(Scene):
        def construct(self):
            tex = Tex(r'$x^2 + y^2 = z^2$', tex_template=TexFontTemplates.french_cursive).scale(3)
            self.add(tex)

Manim also has a :class:`~.TexTemplateLibrary` containing the TeX templates used by 3Blue1Brown. One example
is the ctex template, used for typesetting Chinese. For this to work, the ctex LaTeX package
must be installed on your system. Furthermore, if you are only typesetting Text, you probably do not
need :class:`~.Tex` at all, and should use :class:`~.Text` or :class:`~.PangoText` instead.

.. manim:: LaTeXTemplateLibrary
    :save_last_frame:

    class LaTeXTemplateLibrary(Scene):
        def construct(self):
            tex = Tex('Hello 你好 \\LaTeX', tex_template=TexTemplateLibrary.ctex).scale(3)
            self.add(tex)


Aligning formulae
+++++++++++++++++
A :class:`~.MathTex` mobject is typeset in the LaTeX  ``align*`` environment. This means you can use the ``&`` alignment
character when typesetting multiline formulae:

.. manim:: LaTeXAlignEnvironment
    :save_last_frame:

    class LaTeXAlignEnvironment(Scene):
        def construct(self):
            tex = MathTex(r'f(x) &= 3 + 2 + 1\\ &= 5 + 1 \\ &= 6').scale(2)
            self.add(tex)
"""

__all__ = [
    "TexSymbol",
    "SingleStringMathTex",
    "MathTex",
    "Tex",
    "BulletedList",
    "Title",
]


import itertools as it
import operator as op
import re
from functools import reduce
from textwrap import dedent

from colour import Color

from ... import config, logger
from ...constants import *
from ...mobject.geometry import Line
from ...mobject.svg.svg_mobject import SVGMobject
from ...mobject.svg.svg_path import SVGPathMobject
from ...mobject.types.vectorized_mobject import VectorizedPoint, VGroup
from ...utils.color import BLACK, WHITE
from ...utils.tex import TexTemplate
from ...utils.tex_file_writing import tex_to_svg_file
from .style_utils import parse_style

TEX_MOB_SCALE_FACTOR = 0.05


class TexSymbol(SVGPathMobject):
    """Purely a renaming of SVGPathMobject."""

    pass


class SingleStringMathTex(SVGMobject):
    """Elementary building block for rendering text with LaTeX.

    Tests
    -----
    Check that creating a :class:`~.SingleStringMathTex` object works::

        >>> SingleStringMathTex('Test') # doctest: +SKIP
        SingleStringMathTex('Test')
    """

    def __init__(
        self,
        tex_string,
        stroke_width=0,
        fill_opacity=1.0,
        background_stroke_width=0,
        background_stroke_color=BLACK,
        should_center=True,
        height=None,
        organize_left_to_right=False,
        tex_environment="align*",
        tex_template=None,
        color=Color(WHITE),
        **kwargs,
    ):
        self.organize_left_to_right = organize_left_to_right
        self.tex_environment = tex_environment
        if tex_template is None:
            tex_template = config["tex_template"]
        self.tex_template = tex_template

        assert isinstance(tex_string, str)
        self.tex_string = tex_string
        file_name = tex_to_svg_file(
            self.get_modified_expression(tex_string),
            environment=self.tex_environment,
            tex_template=self.tex_template,
        )
        SVGMobject.__init__(
            self,
            file_name=file_name,
            should_center=should_center,
            stroke_width=stroke_width,
            height=height,
            fill_opacity=fill_opacity,
            background_stroke_width=background_stroke_width,
            background_stroke_color=background_stroke_color,
            should_subdivide_sharp_curves=True,
            should_remove_null_curves=True,
            color=color,
            **kwargs,
        )
        if height is None:
            self.scale(TEX_MOB_SCALE_FACTOR)
        if self.organize_left_to_right:
            self.organize_submobjects_left_to_right()

    def __repr__(self):
        return f"{type(self).__name__}({repr(self.tex_string)})"

    def get_modified_expression(self, tex_string):
        result = tex_string
        result = result.strip()
        result = self.modify_special_strings(result)
        return result

    def modify_special_strings(self, tex):
        tex = tex.strip()
        should_add_filler = reduce(
            op.or_,
            [
                # Fraction line needs something to be over
                tex == "\\over",
                tex == "\\overline",
                # Make sure sqrt has overbar
                tex == "\\sqrt",
                tex == "\\sqrt{",
                # Need to add blank subscript or superscript
                tex.endswith("_"),
                tex.endswith("^"),
                tex.endswith("dot"),
            ],
        )

        if should_add_filler:
            filler = "{\\quad}"
            tex += filler

        if tex == "\\substack":
            tex = "\\quad"

        if tex == "":
            tex = "\\quad"

        # To keep files from starting with a line break
        if tex.startswith("\\\\"):
            tex = tex.replace("\\\\", "\\quad\\\\")

        # Handle imbalanced \left and \right
        num_lefts, num_rights = [
            len([s for s in tex.split(substr)[1:] if s and s[0] in "(){}[]|.\\"])
            for substr in ("\\left", "\\right")
        ]
        if num_lefts != num_rights:
            tex = tex.replace("\\left", "\\big")
            tex = tex.replace("\\right", "\\big")

        tex = self.remove_stray_braces(tex)

        for context in ["array"]:
            begin_in = ("\\begin{%s}" % context) in tex
            end_in = ("\\end{%s}" % context) in tex
            if begin_in ^ end_in:
                # Just turn this into a blank string,
                # which means caller should leave a
                # stray \\begin{...} with other symbols
                tex = ""
        return tex

    def remove_stray_braces(self, tex):
        r"""
        Makes :class:`~.MathTex` resilient to unmatched braces.

        This is important when the braces in the TeX code are spread over
        multiple arguments as in, e.g., ``MathTex(r"e^{i", r"\tau} = 1")``.
        """

        # "\{" does not count (it's a brace literal), but "\\{" counts (it's a new line and then brace)
        num_lefts = tex.count("{") - tex.count("\\{") + tex.count("\\\\{")
        num_rights = tex.count("}") - tex.count("\\}") + tex.count("\\\\}")
        while num_rights > num_lefts:
            tex = "{" + tex
            num_lefts += 1
        while num_lefts > num_rights:
            tex = tex + "}"
            num_rights += 1
        return tex

    def get_tex_string(self):
        return self.tex_string

    def path_string_to_mobject(self, path_string, style):
        # Overwrite superclass default to use
        # specialized path_string mobject
        return TexSymbol(path_string, **self.path_string_config, **parse_style(style))

    def organize_submobjects_left_to_right(self):
        self.sort(lambda p: p[0])
        return self

    def init_colors(self, propagate_colors=True):
        super().init_colors(propagate_colors=propagate_colors)


class MathTex(SingleStringMathTex):
    r"""A string compiled with LaTeX in math mode.

    Examples
    --------
    .. manim:: Formula
        :save_last_frame:

        class Formula(Scene):
            def construct(self):
                t = MathTex(r"\int_a^b f'(x) dx = f(b)- f(a)")
                self.add(t)

    Tests
    -----
    Check that creating a :class:`~.MathTex` works::

        >>> MathTex('a^2 + b^2 = c^2') # doctest: +SKIP
        MathTex('a^2 + b^2 = c^2')

    Check that double brace group splitting works correctly::

        >>> t1 = MathTex('{{ a }} + {{ b }} = {{ c }}') # doctest: +SKIP
        >>> len(t1.submobjects) # doctest: +SKIP
        5
        >>> t2 = MathTex(r"\frac{1}{a+b\sqrt{2}}") # doctest: +SKIP
        >>> len(t2.submobjects) # doctest: +SKIP
        1

    """

    def __init__(
        self,
        *tex_strings,
        arg_separator=" ",
        substrings_to_isolate=None,
        tex_to_color_map=None,
        tex_environment="align*",
        **kwargs,
    ):
        self.tex_template = kwargs.pop("tex_template", config["tex_template"])
        self.arg_separator = arg_separator
        self.substrings_to_isolate = (
            [] if substrings_to_isolate is None else substrings_to_isolate
        )
        self.tex_to_color_map = tex_to_color_map
        if self.tex_to_color_map is None:
            self.tex_to_color_map = {}
        self.tex_environment = tex_environment
        self.brace_notation_split_occurred = False
        tex_strings = self.break_up_tex_strings(tex_strings)
        self.tex_strings = tex_strings
        try:
            SingleStringMathTex.__init__(
                self,
                self.arg_separator.join(tex_strings),
                tex_environment=self.tex_environment,
                tex_template=self.tex_template,
                **kwargs,
            )
            self.break_up_by_substrings()
        except ValueError as compilation_error:
            if self.brace_notation_split_occurred:
                logger.error(
                    dedent(
                        """\
                        A group of double braces, {{ ... }}, was detected in
                        your string. Manim splits TeX strings at the double
                        braces, which might have caused the current
                        compilation error. If you didn't use the double brace
                        split intentionally, add spaces between the braces to
                        avoid the automatic splitting: {{ ... }} --> { { ... } }.
                        """
                    )
                )
            raise compilation_error
        self.set_color_by_tex_to_color_map(self.tex_to_color_map)

        if self.organize_left_to_right:
            self.organize_submobjects_left_to_right()

    def break_up_tex_strings(self, tex_strings):
        # Separate out anything surrounded in double braces
        pre_split_length = len(tex_strings)
        tex_strings = [re.split("{{(.*?)}}", str(t)) for t in tex_strings]
        tex_strings = sum(tex_strings, [])
        if len(tex_strings) > pre_split_length:
            self.brace_notation_split_occurred = True

        # Separate out any strings specified in the isolate
        # or tex_to_color_map lists.
        patterns = []
        patterns.extend(
            [
                "({})".format(re.escape(ss))
                for ss in it.chain(
                    self.substrings_to_isolate, self.tex_to_color_map.keys()
                )
            ]
        )
        pattern = "|".join(patterns)
        if pattern:
            pieces = []
            for s in tex_strings:
                pieces.extend(re.split(pattern, s))
        else:
            pieces = tex_strings
        return [p for p in pieces if p]

    def break_up_by_substrings(self):
        """
        Reorganize existing submobjects one layer
        deeper based on the structure of tex_strings (as a list
        of tex_strings)
        """
        new_submobjects = []
        curr_index = 0
        for tex_string in self.tex_strings:
            sub_tex_mob = SingleStringMathTex(
                tex_string,
                tex_environment=self.tex_environment,
                tex_template=self.tex_template,
            )
            num_submobs = len(sub_tex_mob.submobjects)
            new_index = (
                curr_index + num_submobs + len("".join(self.arg_separator.split()))
            )
            if num_submobs == 0:
                # For cases like empty tex_strings, we want the corresponding
                # part of the whole MathTex to be a VectorizedPoint
                # positioned in the right part of the MathTex
                sub_tex_mob.submobjects = [VectorizedPoint()]
                if config.renderer == "opengl":
                    sub_tex_mob.assemble_family()
                last_submob_index = min(curr_index, len(self.submobjects) - 1)
                sub_tex_mob.move_to(self.submobjects[last_submob_index], RIGHT)
            else:
                sub_tex_mob.submobjects = self.submobjects[curr_index:new_index]
                if config.renderer == "opengl":
                    sub_tex_mob.assemble_family()
            new_submobjects.append(sub_tex_mob)
            curr_index = new_index
        self.submobjects = new_submobjects
        if config.renderer == "opengl":
            self.assemble_family()
        return self

    def get_parts_by_tex(self, tex, substring=True, case_sensitive=True):
        def test(tex1, tex2):
            if not case_sensitive:
                tex1 = tex1.lower()
                tex2 = tex2.lower()
            if substring:
                return tex1 in tex2
            else:
                return tex1 == tex2

        return VGroup(*[m for m in self.submobjects if test(tex, m.get_tex_string())])

    def get_part_by_tex(self, tex, **kwargs):
        all_parts = self.get_parts_by_tex(tex, **kwargs)
        return all_parts[0] if all_parts else None

    def set_color_by_tex(self, tex, color, **kwargs):
        parts_to_color = self.get_parts_by_tex(tex, **kwargs)
        for part in parts_to_color:
            part.set_color(color)
        return self

    def set_color_by_tex_to_color_map(self, texs_to_color_map, **kwargs):
        for texs, color in list(texs_to_color_map.items()):
            try:
                # If the given key behaves like tex_strings
                texs + ""
                self.set_color_by_tex(texs, color, **kwargs)
            except TypeError:
                # If the given key is a tuple
                for tex in texs:
                    self.set_color_by_tex(tex, color, **kwargs)
        return self

    def index_of_part(self, part):
        split_self = self.split()
        if part not in split_self:
            raise ValueError("Trying to get index of part not in MathTex")
        return split_self.index(part)

    def index_of_part_by_tex(self, tex, **kwargs):
        part = self.get_part_by_tex(tex, **kwargs)
        return self.index_of_part(part)

    def sort_alphabetically(self):
        self.submobjects.sort(key=lambda m: m.get_tex_string())


class Tex(MathTex):
    r"""A string compiled with LaTeX in normal mode.

    Tests
    -----

    Check whether writing a LaTeX string works::

        >>> Tex('The horse does not eat cucumber salad.') # doctest: +SKIP
        Tex('The horse does not eat cucumber salad.')

    """

    def __init__(
        self, *tex_strings, arg_separator="", tex_environment="center", **kwargs
    ):
        MathTex.__init__(
            self,
            *tex_strings,
            arg_separator=arg_separator,
            tex_environment=tex_environment,
            **kwargs,
        )


class BulletedList(Tex):
    """
    Examples
    --------

    .. manim:: BulletedListExample
        :save_last_frame:

        class BulletedListExample(Scene):
            def construct(self):
                blist = BulletedList("Item 1", "Item 2", "Item 3", height=2, width=2)
                blist.set_color_by_tex("Item 1", RED)
                blist.set_color_by_tex("Item 2", GREEN)
                blist.set_color_by_tex("Item 3", BLUE)
                self.add(blist)
    """

    def __init__(
        self,
        *items,
        buff=MED_LARGE_BUFF,
        dot_scale_factor=2,
        tex_environment=None,
        **kwargs,
    ):
        self.buff = buff
        self.dot_scale_factor = dot_scale_factor
        self.tex_environment = tex_environment
        line_separated_items = [s + "\\\\" for s in items]
        Tex.__init__(
            self, *line_separated_items, tex_environment=tex_environment, **kwargs
        )
        for part in self:
            dot = MathTex("\\cdot").scale(self.dot_scale_factor)
            dot.next_to(part[0], LEFT, SMALL_BUFF)
            part.add_to_back(dot)
        self.arrange(DOWN, aligned_edge=LEFT, buff=self.buff)

    def fade_all_but(self, index_or_string, opacity=0.5):
        arg = index_or_string
        if isinstance(arg, str):
            part = self.get_part_by_tex(arg)
        elif isinstance(arg, int):
            part = self.submobjects[arg]
        else:
            raise TypeError(f"Expected int or string, got {arg}")
        for other_part in self.submobjects:
            if other_part is part:
                other_part.set_fill(opacity=1)
            else:
                other_part.set_fill(opacity=opacity)


class Title(Tex):
    """
    Examples
    --------
    .. manim:: TitleExample
        :save_last_frame:

        import manim

        class TitleExample(Scene):
            def construct(self):
                banner = ManimBanner()
                title = Title(f"Manim version {manim.__version__}")
                self.add(banner, title)

    """

    def __init__(
        self,
        *text_parts,
        scale_factor=1,
        include_underline=True,
        match_underline_width_to_text=False,
        underline_buff=MED_SMALL_BUFF,
        **kwargs,
    ):
        self.scale_factor = scale_factor
        self.include_underline = include_underline
        self.match_underline_width_to_text = match_underline_width_to_text
        self.underline_buff = underline_buff
        Tex.__init__(self, *text_parts, **kwargs)
        self.scale(self.scale_factor)
        self.to_edge(UP)
        if self.include_underline:
            underline_width = config["frame_width"] - 2
            underline = Line(LEFT, RIGHT)
            underline.next_to(self, DOWN, buff=self.underline_buff)
            if self.match_underline_width_to_text:
                underline.match_width(self)
            else:
                underline.width = underline_width
            self.add(underline)
            self.underline = underline
