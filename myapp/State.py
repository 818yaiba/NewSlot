class State:
    """
    状態

    Attributes
    ----------
    id : int
        状態ID
    name : str
        状態名
    """

    id = 0

    def __init__(self, name: str):
        """
        Parameters
        ----------
        name : str
            状態名
        """
        self.id = State.id
        State.id += 1
        self.name = name
