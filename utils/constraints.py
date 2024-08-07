COLUMNS = {
    1: [
        "max_loss",
        "max_loss_close",
        "buying_power",
    ],
    2: ["max_loss_close", "day_pos_investment"],
    3: [
        "day_pos_investment",
    ],
}


def get_constraints(num: int) -> list | None:
    return COLUMNS.get(num)
