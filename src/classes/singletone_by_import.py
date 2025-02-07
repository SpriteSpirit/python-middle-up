from singletone_as_default_module import person

bob = person
alice = person

print(bob is alice)  # Output: True - это один и тот же экземпляр
print(bob.name)  # Output: Bob
print(alice.name)  # Output: Bob
