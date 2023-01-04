from salad_parser import FoodParser

foods = {
    525: 'kotletos',
    527: 'salatos',
}


if __name__ == '__main__':
    for food_id, food_name in foods.items():
        salad_parser = FoodParser(food_id)
        salad_parser.run()
        salad_parser.save_to_json(food_name)
