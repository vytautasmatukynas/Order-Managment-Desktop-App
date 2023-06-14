import ctypes


class scaling_dpi():

    def __init__(self):
        # get windows scale ratio
        user32 = ctypes.windll.user32

        self.scale_factor = user32.GetDpiForSystem() / 96.0
        # print("Scale factor:", self.scale_factor)

        # change widget size to scale ratio
        self.TEXT_PT = int(12 * self.scale_factor)
        self.BUTTON_HEIGHT = int(25 * self.scale_factor)
        self.ENTRY_COMBO_HEIGHT = int(25 * self.scale_factor)
        self.SEARCH_BUTTON_WIDTH = int(90 * self.scale_factor)
        self.PROGRESS_WIDTH = int(150 * self.scale_factor)
        self.TREE_TABLE_WIDTH = int(150 * self.scale_factor)
        self.TB_ICON_WIDTH = int(17 * self.scale_factor)
        self.TB_ICON_HEIGHT = int(17 * self.scale_factor)
