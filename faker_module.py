from faker import Faker

fake = Faker()

my_var = fake.sentence(nb_words=10)

print(my_var)

