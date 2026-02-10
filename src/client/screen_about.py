from textual import events
from textual.app import ComposeResult
from textual.widgets import Footer
from textual.screen import Screen
from textual.widgets import Label


class AboutScreen(Screen):

    CSS = """
        Screen {
            align: center middle;
        }
        """
    BINDINGS = [
        ("[Tab]", "Return", "Go back to the main menu!",),
    ]

    about_page = """ 
                                                                    Hello!
                                                                    
                                                                    
                    First of all I want to thank you for using this, it genuinely means the world to me and it would not be possible without you!
                    Also if there are any bugs, you have questions, or anything like that (or if you simply want to say hi hehe)
                    check at the bottom of this message for my discord, email, and link to the GitHub repository of this project.


                    Some of the key features of this little app is that it is a terminal application, (basically its not technically a GUI), that it is
                    open source, and honestly just something I wanted to make since networking is really frigging kewl! 
                    
                    
                    Some others reasons I made this is because I want to be able to communicate on something that is *truly* free and open, which I really
                    hope this can accomplish.
                    
                    Some shoutouts here are:
                    
                    -       The textual TUI library I’ve extensively used
                    
                    -       Victoria2048, a collaborator and friend of mine (their GitHub is  “https://github.com/Victoria2048”)
                    
                    -       The GNU project for all their open source contributions and the license I use for this project
                    
                    -       And of course last but certainly not least, you! I know I already thanked you but I simply cannot stress enough how much it means 
                            that you are even reading this!
                    
                    My contacts!
                    Discord: victoria_91223 (discord, ironic right?)
                    Email: gameboynes2@pm.me (shush its a good email name)
                    GitHub repo: https://github.com/mynameisVictoria/plan-9-from-cx 
                    """

    def compose(self) -> ComposeResult:
        yield Label(f"{self.about_page}", id="main_menu")
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        if event.key == "tab":
            self.app.pop_screen()
            self.app.push_screen("menu")
