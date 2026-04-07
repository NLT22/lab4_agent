from langchain_core.tools import tool

# =========================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# =========================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.

    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')

    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé một chiều.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    try:
        flights = FLIGHTS_DB.get((origin, destination))
        route_origin = origin
        route_destination = destination

        if not flights:
            flights = FLIGHTS_DB.get((destination, origin))
            if flights:
                route_origin = destination
                route_destination = origin

        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

        def format_price(price: int) -> str:
            return f"{price:,}".replace(",", ".") + "đ"

        lines = [
            f"Các chuyến bay từ {route_origin} đến {route_destination} (giá dưới đây là giá vé một chiều):"
        ]
        for index, flight in enumerate(flights, start=1):
            lines.append(
                f"{index}. {flight['airline']} | {flight['departure']} - {flight['arrival']} | "
                f"{flight['class']} | {format_price(flight['price'])}"
            )
        return "\n".join(lines)
    except (KeyError, TypeError, ValueError):
        return "Đã xảy ra lỗi khi tìm kiếm chuyến bay. Vui lòng thử lại."


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn

    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    Lưu ý: giá trả về là giá mỗi đêm. Nếu người dùng ở nhiều đêm, cần nhân đúng
    số đêm trước khi truyền chi phí vào calculate_budget.
    """
    try:
        hotels = HOTELS_DB.get(city, [])
        filtered_hotels = [
            hotel for hotel in hotels if hotel["price_per_night"] <= max_price_per_night
        ]
        filtered_hotels.sort(key=lambda hotel: hotel["rating"], reverse=True)

        def format_price(price: int) -> str:
            return f"{price:,}".replace(",", ".") + "đ"

        if not filtered_hotels:
            return (
                f"Không tìm thấy khách sạn tại {city} với giá dưới "
                f"{format_price(max_price_per_night)}/đêm."
            )

        lines = [
            (
                f"Danh sách khách sạn tại {city} "
                f"(giá tối đa {format_price(max_price_per_night)}/đêm, "
                "mọi mức giá bên dưới đều là giá mỗi đêm):"
            )
        ]
        for index, hotel in enumerate(filtered_hotels, start=1):
            lines.append(
                f"{index}. {hotel['name']} | {hotel['stars']} sao | "
                f"{hotel['area']} | rating {hotel['rating']} | "
                f"{format_price(hotel['price_per_night'])}/đêm"
            )
        return "\n".join(lines)
    except (KeyError, TypeError, ValueError):
        return "Đã xảy ra lỗi khi tìm kiếm khách sạn. Vui lòng thử lại."


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: ve_may_bay:890000,khach_san:650000)

    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """

    def format_price(price: int) -> str:
        return f"{price:,}".replace(",", ".") + "đ"

    expense_items = []
    total_expense = 0

    try:
        raw_items = [item.strip() for item in expenses.split(",") if item.strip()]
        for raw_item in raw_items:
            name, amount_text = [part.strip() for part in raw_item.split(":", 1)]
            if not name or not amount_text:
                raise ValueError

            amount = int(amount_text)
            if amount < 0:
                raise ValueError

            expense_items.append((name, amount))
            total_expense += amount
    except (ValueError, TypeError):
        return (
            "Dữ liệu chi phí không hợp lệ. Vui lòng nhập theo định dạng "
            "'ten_khoan:so_tien', các khoản cách nhau bằng dấu phẩy."
        )

    remaining_budget = total_budget - total_expense

    lines = [f"Ngân sách ban đầu: {format_price(total_budget)}", "Chi tiết chi phí:"]
    if expense_items:
        for index, (name, amount) in enumerate(expense_items, start=1):
            lines.append(f"{index}. {name}: {format_price(amount)}")
    else:
        lines.append("Không có khoản chi nào.")

    lines.append(f"Tổng chi phí: {format_price(total_expense)}")

    if remaining_budget < 0:
        lines.append(
            f"Vượt ngân sách {format_price(-remaining_budget)}! Cần điều chỉnh."
        )
    else:
        lines.append(f"Số tiền còn lại: {format_price(remaining_budget)}")

    return "\n".join(lines)
