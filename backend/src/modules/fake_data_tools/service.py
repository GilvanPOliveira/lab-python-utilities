import json
import random
import string


LOREM_SENTENCES = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Integer vitae lorem non massa viverra malesuada.",
    "Suspendisse potenti, sed facilisis justo interdum non.",
    "Praesent euismod, justo vitae viverra tincidunt, nisl nunc porta risus.",
    "Donec a sem at magna consequat posuere.",
    "Aliquam erat volutpat, sed dignissim purus dictum nec.",
    "Curabitur posuere metus nec magna tincidunt, in luctus justo viverra.",
    "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.",
]

FIRST_NAMES = [
    "Ana",
    "Bruno",
    "Carla",
    "Diego",
    "Fernanda",
    "Gilvan",
    "Helena",
    "Igor",
    "Juliana",
    "Lucas",
    "Marina",
    "Rafael",
]

LAST_NAMES = [
    "Oliveira",
    "Silva",
    "Santos",
    "Ferreira",
    "Almeida",
    "Costa",
    "Lima",
    "Barbosa",
    "Pereira",
    "Gomes",
]

DOMAINS = [
    "example.com",
    "mail.com",
    "teste.dev",
    "demo.com",
]


def generate_lorem(paragraphs: int) -> dict:
    generated = []

    for _ in range(paragraphs):
        sentence_count = random.randint(3, 6)
        paragraph = " ".join(random.choice(LOREM_SENTENCES) for _ in range(sentence_count))
        generated.append(paragraph)

    return {
        "result": "\n\n".join(generated),
    }


def generate_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def slugify_name(name: str) -> str:
    return name.lower().replace(" ", ".")


def generate_email(name: str | None = None) -> str:
    selected_name = name or generate_name()
    random_number = random.randint(10, 999)
    return f"{slugify_name(selected_name)}{random_number}@{random.choice(DOMAINS)}"


def generate_phone() -> str:
    ddd = random.randint(11, 99)
    part_one = random.randint(90000, 99999)
    part_two = random.randint(1000, 9999)

    return f"({ddd}) {part_one}-{part_two}"


def generate_password(length: int = 12) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def generate_names(quantity: int) -> dict:
    return {
        "result": "\n".join(generate_name() for _ in range(quantity)),
    }


def generate_emails(quantity: int) -> dict:
    return {
        "result": "\n".join(generate_email() for _ in range(quantity)),
    }


def generate_phones(quantity: int) -> dict:
    return {
        "result": "\n".join(generate_phone() for _ in range(quantity)),
    }


def generate_fake_json(quantity: int) -> dict:
    data = []

    for index in range(quantity):
        name = generate_name()

        data.append(
            {
                "id": index + 1,
                "name": name,
                "email": generate_email(name),
                "phone": generate_phone(),
                "active": random.choice([True, False]),
            }
        )

    return {
        "result": json.dumps(data, ensure_ascii=False, indent=2),
    }
