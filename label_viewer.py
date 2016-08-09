import wx


class LabelViewerPanel(wx.Panel):
    """
    Parent class for other custom panels. Hides the cursor and handles
    keypress events.
    """

    def __init__(self, parent, image, name, panel_size):
        wx.Panel.__init__(self, parent, size=panel_size)
        self.frame = parent
        self.name = name
        self.Bind(wx.EVT_CHAR, self.on_keypress)
        self.cursor = wx.StockCursor(wx.CURSOR_BLANK)
        self.BackgroundColour = wx.BLACK
        self.widgets = []
        self.image = image
        # Uncomment the following line on wxpython 2.x
        # self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.draw_image)

    def hide_cursor(self):
        for widget in self.widgets:
            widget.SetCursor(self.cursor)

    def on_keypress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.frame.close()

    def draw_image(self, event):
        """
        Draws the image to the panel's background.
        """
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        image = wx.Bitmap(self.image)
        dc.DrawBitmap(image, 0, 0)
        self.SetFocus()

    def switch_panel(self, event):
        self.frame.switch_panel(self.name, event.GetEventObject().GetName())

    def add_button(self, image_path, img_name, position):
        image_path = './images/' + image_path
        bmp = wx.Bitmap(image_path, wx.BITMAP_TYPE_PNG)
        widget = wx.StaticBitmap(self, name=img_name, pos=position, bitmap=bmp)
        widget.Bind(wx.EVT_LEFT_DOWN, self.switch_panel)
        self.widgets.append(widget)


class MainPanel(LabelViewerPanel):
    """
    Main shelf panel. When touched/clicked each object opens a new panel.
    """

    def __init__(self, parent, image, name, panel_size):
        LabelViewerPanel.__init__(self, parent, image, name, panel_size)

        self.add_button('shelf/glass.png', 'glass', (936, 290))
        self.add_button('shelf/paper.png', 'paper', (935, 665))
        self.add_button('shelf/seeds.png', 'seeds', (720, 895))
        self.add_button('shelf/snail_shell.png', 'snail_shell', (936, 766))
        self.add_button('shelf/silver_turquoise.png', 'silver_turquoise', (737, 770))
        self.add_button('shelf/birch_bark.png', 'birch_bark', (800, 530))
        self.add_button('shelf/ceramic.png', 'ceramic', (935, 530))
        self.add_button('shelf/eggshell.png', 'eggshell', (936, 50))
        self.add_button('shelf/duiker_hoof.png', 'duiker_hoof', (430, 50))
        self.add_button('shelf/glass_teeth.png', 'glass_teeth', (430, 290))
        self.add_button('shelf/jade.png', 'jade', (470, 810))
        self.add_button('shelf/leather.png', 'leather', (690, 300))
        self.add_button('shelf/wood.png', 'wood', (670, 530))
        self.add_button('shelf/metal.png', 'metal', (690, 420))
        self.add_button('shelf/stone.png', 'stone', (540, 770))
        self.add_button('shelf/ivory.png', 'ivory', (435, 530))

        self.hide_cursor()
        self.SetFocus()


class LabelPanel(LabelViewerPanel):
    """
    A detailed object panel. Contains information and additional images about
    the object.
    """

    def __init__(self, parent, background, name, next_panel, panel_size):
        LabelViewerPanel.__init__(self, parent, background, name, panel_size)

        # Buttons
        self.add_button('buttons/zoom.png', name + '_zoom', (50, 950))
        self.add_button('buttons/next.png', next_panel, (250, 950))
        self.add_button('buttons/home.png', 'main', (450, 950))

        self.hide_cursor()


class IvoryPanel(LabelViewerPanel):
    """
    An unique panel for the ivory necklace with additional image button. Contains information and additional images
    about the object.
    """

    def __init__(self, parent, background, images, name, next_panel, img_dest, panel_size):
        LabelViewerPanel.__init__(self, parent, background, name, panel_size)

        # Images
        self.add_button(images[0][0], img_dest, images[0][1])

        # Buttons
        self.add_button('buttons/zoom.png', name + '_zoom', (50, 950))
        self.add_button('buttons/next.png', next_panel, (250, 950))
        self.add_button('buttons/home.png', 'main', (450, 950))

        self.hide_cursor()


class ZoomPanel(LabelViewerPanel):
    """
    A zoomed object panel.
    """

    def __init__(self, parent, image, name, src_name, panel_size):
        LabelViewerPanel.__init__(self, parent, image, name, panel_size)

        # Buttons
        self.add_button('buttons/return.png', src_name, (50, 950))

        self.hide_cursor()


class MainFrame(wx.Frame):
    """
    Main panel frame. Switches between panels.
    """

    def __init__(self, parent, image_size):
        wx.Frame.__init__(self, parent, wx.ID_ANY, size=image_size)
        self.size = image_size
        self.ShowFullScreen(True, style=wx.FULLSCREEN_ALL)
        self.BackgroundColour = wx.BLACK
        self.panels = []
        self.panel_dict = {}

        main_panel = MainPanel(self, './images/shelf/background.png', 'main', image_size)
        self.panel_dict['main'] = main_panel

        self.add_panel('duiker_hoof', 'eggshell')
        self.add_panel('eggshell', 'glass_teeth')
        self.add_panel('glass_teeth', 'leather')
        self.add_panel('leather', 'metal')
        self.add_panel('metal', 'glass')
        self.add_panel('glass', 'ivory')

        images = [['ivory1/walrus.png', (868, 629)]]
        self.add_ivory_panel('ivory1/background.png', images, 'ivory', 'wood', 'ivory2')
        self.add_zoom_panel('ivory1/ivory.png', 'ivory_zoom', 'ivory')

        self.add_panel('ivory2', 'wood')
        self.add_panel('wood', 'birch_bark')
        self.add_panel('birch_bark', 'ceramic')
        self.add_panel('ceramic', 'paper')
        self.add_panel('paper', 'jade')
        self.add_panel('jade', 'stone')
        self.add_panel('stone', 'silver_turquoise')
        self.add_panel('silver_turquoise', 'seeds')
        self.add_panel('seeds', 'snail_shell')
        self.add_panel('snail_shell', 'duiker_hoof')

        # Timer to switch back to main shelf
        self.timeout = 600000  # 10 min
        self.timeout_timer = wx.Timer(self, wx.ID_ANY)
        self.start_timeout_timer()

        self.current_panel = 'main'

    def add_panel(self, name, next_panel):
        self.add_label_panel(name + '/background.png', name, next_panel)
        self.add_zoom_panel(name + '/' + name + '.png', name + '_zoom', name)

    def add_ivory_panel(self, background, images, name, next_panel, img_dest):
        bg = './images/' + background
        panel = IvoryPanel(self, bg, images, name, next_panel, img_dest, self.size)
        panel.name = name
        panel.Hide()
        self.panel_dict[name] = panel

    def add_label_panel(self, background, name, next_panel):
        bg = './images/' + background
        panel = LabelPanel(self, bg, name, next_panel, self.size)
        panel.Hide()
        self.panel_dict[name] = panel

    def add_zoom_panel(self, image, name, src_name):
        background = './images/' + image
        panel = ZoomPanel(self, background, name, src_name, self.size)
        panel.Hide()
        self.panel_dict[name] = panel

    def switch_panel(self, src_id, dest_id):
        self.panel_dict[src_id].Hide()
        self.panel_dict[dest_id].Show()
        self.panel_dict[dest_id].SetFocus()
        self.current_panel = dest_id
        self.Layout()
        self.restart_timeout_timer()

    def start_timeout_timer(self):
        self.Bind(wx.EVT_TIMER, self.switch_on_timeout, self.timeout_timer)
        self.timeout_timer.Start(self.timeout)

    def restart_timeout_timer(self):
        self.timeout_timer.Stop()
        self.start_timeout_timer()

    def switch_on_timeout(self, event):
        self.switch_panel(self.current_panel, 'main')
        self.restart_timeout_timer()

    def close(self):
        self.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    MainFrame(None, (1920, 1080)).Show()
    app.MainLoop()
