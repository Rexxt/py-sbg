class Generator:
    def __init__(self, gen_dir:str):
        """Static site generator

        Args:
            gen_dir (str): the directory to generate to
        """
        self.gen_dir = gen_dir

    def make_page(self, name, function, data=None):
        with open(f'{self.gen_dir}/{name}.html', 'w') as f:
            f.write(function(data))