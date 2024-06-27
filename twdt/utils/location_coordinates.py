from typing import TypedDict

from twdt.models import Warehouse, Rack, RackLocation


class GenerateLocationCoordinatesProps(TypedDict):
    rack_columns: str
    rack_column_distance: str
    rack_depth: str
    rack_depth_distance: str
    rack_level1_height: str
    rack_levels: str
    rack_level_distance: str
    rack_no: str
    reference_x: str
    reference_y: str
    reference_z: str
    warehouse_code: str
    warehouse_level: str


def get_offset_z(*, level: int, reference: float, rack_level_distance: float, rack_level1_height: float) -> float:
    if level == 1:
        return 0
    if level == 2:
        return rack_level1_height
    return rack_level1_height + (level -2) * rack_level_distance


def generate_location_coordinates(data: GenerateLocationCoordinatesProps) -> int:
    warehouse_code: str = data["warehouse_code"]
    warehouse: Warehouse | None = Warehouse.objects.filter(warehouse_code=warehouse_code).first()
    if not warehouse: raise Exception(f"Invalid warehouse: {warehouse_code}")

    rack_no: int = int(data["rack_no"])
    rack: Rack | None = Rack.objects.filter(rack_no=rack_no).first()
    if not rack: raise Exception(f"Invalid rack#: {rack_no}")


    rack_column_distance: float = float(data["rack_column_distance"])
    rack_depth_distance: float = float(data["rack_depth_distance"])
    rack_level1_height: float = float(data["rack_level1_height"])
    rack_level_distance: float = float(data["rack_level_distance"])

    reference_x: float = float(data["reference_x"])
    reference_y: float = float(data["reference_y"])
    reference_z: float = float(data["reference_z"])

    warehouse_level: int = int(data["warehouse_level"])
    count: int = 0

    for level in range(1, int(data["rack_levels"]) + 1):
        for column in range(1, int(data["rack_columns"]) + 1):
            for depth in range(1, int(data["rack_depth"]) + 1):
                location_id: str = (
                    f"{warehouse_level}"
                    f"{rack_no:02}"
                    f"{level}"
                    f"{column:02}"
                    f"{depth}"
                )
                offset_x: float = reference_x + (column - 1) * rack_column_distance
                offset_y: float = reference_y + (depth - 1) * rack_depth_distance
                offset_z: float = get_offset_z(
                    level=level,
                    reference=reference_z ,
                    rack_level_distance=rack_level_distance,
                    rack_level1_height=rack_level1_height,
                )
                RackLocation.objects.update_or_create(
                    location_id=location_id,
                    defaults={
                        "rack": rack,
                        "coordinates": {
                            "x": reference_x + offset_x,
                            "y": reference_y + offset_y,
                            "z": reference_z + offset_z,
                        }
                    },
                )
                count += 1

    return count
