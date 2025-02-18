recipe_list = []

def get_last_id():
    """
    first we define recipe list so that we can store the recipes in the application memory.
    Then, we define get_last_id function to get the ID of our last recipe.
    Later, when we are create a new recipe, we will use this method to evaluate the last ID in recipe_list so that we can come up with a new ID for the new recipe.
    """
    if recipe_list:
        last_recipe = recipe_list[-1]
    else:
        return 1
    return last_recipe.id +1


class Recipe:
    def __init__(self, name, description, num_of_servings, cook_time, directions):
        """
        Args:
        name: The name of the recipe.
        description: the description of recipe.
        num_of_servings: The number of servings.
        cook_time: The cooking time required. This is an integer whose units are in seconds.
        directions: The directions.

        The ID is self-incremented and is_publish is set to false by default.
        This means that, by default, the recipe will be set to draft (not published).
        
        return:
        Note
        """
        self.id = get_last_id()
        self.name = name
        self.description = description
        self.num_of_servings = num_of_servings
        self.cook_time = cook_time
        self.directions = directions
        self.is_publish = False


    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'num_of_servings': self.num_of_servings,
            'cook_time': self.cook_time,
            'directions': self.directions
        }
    

    


