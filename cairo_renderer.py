import math

import cairo

from shm_buffer import ShmBuffer

from species import Species

class CairoRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.buffer = ShmBuffer(
            width,
            height,
        )

        self.context = (
            self.buffer.context
        )

    def clear(self):
        context = self.context

        context.save()

        context.set_operator(
            cairo.OPERATOR_SOURCE
        )

        context.set_source_rgba(
            0.0,
            0.0,
            0.0,
            0.0,
        )

        context.paint()

        context.restore()

    def _draw_ghost(self, x, y, scale):
        context = self.context

        context.save()

        context.translate(x, y)
        context.scale(scale, scale)

        context.set_operator(
            cairo.OPERATOR_OVER
        )

        context.set_source_rgba(
            0.95,
            0.95,
            1.0,
            0.95,
        )

        context.move_to(-50, 80)

        context.curve_to(
            -80, 60,
            -100, 30,
            -100, -10,
        )

        context.curve_to(
            -100, -80,
            -55, -120,
            0, -120,
        )

        context.curve_to(
            55, -120,
            100, -80,
            100, -10,
        )

        context.curve_to(
            100, 30,
            80, 60,
            50, 80,
        )

        context.curve_to(
            40, 100,
            30, 120,
            10, 100,
        )

        context.curve_to(
            -5, 85,
            -15, 85,
            -30, 100,
        )

        context.curve_to(
            -50, 120,
            -60, 100,
            -50, 80,
        )

        context.close_path()
        context.fill()

        context.set_source_rgba(
            0.1,
            0.1,
            0.15,
            1.0,
        )

        context.arc(
            -35,
            -30,
            10,
            0,
            math.tau,
        )
        context.fill()

        context.arc(
            35,
            -30,
            10,
            0,
            math.tau,
        )
        context.fill()

        context.restore()

    def _scale_for_monster(self, monster):
        memory_mb = (
            monster.memory
            / 1024
            / 1024
        )

        scale = 0.5 + memory_mb / 500.0

        return min(scale, 1.5)

    def _draw_monster(self, monster):
        scale = self._scale_for_monster(
            monster
        )

        activity = min(
            monster.cpu / 100.0,
            1.0,
        )

        bob = (
            math.sin(monster.phase)
            * (5.0 + activity * 10.0)
        )

        x = monster.x
        y = monster.y + bob

        if monster.species == Species.CRAB:
            self._draw_crab(
                x,
                y,
                scale,
            )

        elif monster.species in (
            Species.SNAKE,
            Species.ROBOT,
            Species.SHELL,
        ):
            self._draw_blob(
                x,
                y,
                scale,
            )

        else:
            self._draw_ghost(
                x,
                y,
                scale,
            )

    def _draw_blob(self, x, y, scale):
        context = self.context

        context.save()

        context.translate(x, y)
        context.scale(scale, scale)

        context.set_operator(
            cairo.OPERATOR_OVER
        )

        context.set_source_rgba(
            0.65,
            0.9,
            0.75,
            0.95,
        )

        context.arc(
            0,
            0,
            60,
            0,
            math.tau,
        )

        context.fill()

        context.set_source_rgba(
            0.1,
            0.1,
            0.15,
            1.0,
        )

        context.arc(
            -20,
            -10,
            7,
            0,
            math.tau,
        )
        context.fill()

        context.arc(
            20,
            -10,
            7,
            0,
            math.tau,
        )
        context.fill()

        context.restore()

    def _draw_crab(self, x, y, scale):
        context = self.context

        context.save()

        context.translate(x, y)
        context.scale(scale, scale)

        context.set_operator(
            cairo.OPERATOR_OVER
        )

        context.set_source_rgba(
            0.9,
            0.4,
            0.35,
            0.95,
        )

        context.arc(
            0,
            0,
            50,
            0,
            math.tau,
        )

        context.fill()

        context.set_line_width(8)

        for direction in (-1, 1):
            context.move_to(
                direction * 35,
                20,
            )

            context.line_to(
                direction * 75,
                45,
            )

            context.stroke()

            context.move_to(
                direction * 30,
                35,
            )

            context.line_to(
                direction * 60,
                70,
            )

            context.stroke()

        context.set_source_rgba(
            0.1,
            0.1,
            0.15,
            1.0,
        )

        context.arc(
            -18,
            -10,
            7,
            0,
            math.tau,
        )
        context.fill()

        context.arc(
            18,
            -10,
            7,
            0,
            math.tau,
        )
        context.fill()

        context.restore()

    def render(self, monsters):
        self.clear()

        for monster in monsters:
            self._draw_monster(monster)

        self.buffer.surface.flush()

    def close(self) -> None:
        self.buffer.close()

    def write_to_png(self, filename):
        self.buffer.surface.write_to_png(
            filename
        )
