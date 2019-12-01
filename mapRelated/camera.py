from loguru import logger

class Camera:
    def __init__(self, width, height, margin=1):
        self.topleft_x = 0
        self.topleft_y = 0
        self.width = width
        self.height = height
        self.margin = margin

    def move_camera(self, trg_x, trg_y, game_map):
        """Move camera so that the player is centered on the terminal.
        Returns boolean whether or not camera actually moves.
        """
        # new camera coordinates (top-left corner of the screen relative to the map)
        # coordinates so that the target is at the center of the screen
        new_x = trg_x - int(self.width / 2)
        new_y = trg_y - int(self.height / 2)

        # make sure the camera doesn't see outside the map
        # if new_x < self.margin:
        #     new_x = self.margin
        # if new_y < self.margin:
        #     new_y = self.margin
        # if new_x > (game_map.width - self.width + self.margin):
        #     new_x = game_map.width - self.width + self.margin
        # if new_y > game_map.height - self.height + self.margin:
        #     new_y = game_map.height - self.height + self.margin

        if new_x == self.topleft_x and new_y == self.topleft_y:
            logger.info('starting point')
            return False  # camera didn't move

        self.topleft_x, self.topleft_y = new_x, new_y
        return True  # camera moved



