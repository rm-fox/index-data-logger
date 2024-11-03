from datetime import datetime
from log_all import LogAllPrices
from log_index import Indices

def main():
    current_dateTime = datetime.now()
    current_time_nanos = int(current_dateTime.timestamp() * 1_000_000_000)

    logging_all = LogAllPrices(current_time_nanos)
    logging_all.save_logging_to_db()

    # H100 Index
    h100_index_x1 = logging_all.generate_gpu_index_price(
        gpu_name='H100',
        gpu_count=1,
        cpu_min=25, 
        cpu_max=33,  # removing outliers
        memory_min=160, 
        memory_max=260,
        removed_instances='pci',
        cpu_divisor=26,
        cpu_weighting=0.2,
        memory_divisor=200,
        memory_weighting=0.1
    )
    print(h100_index_x1)
    h100_index_x8 = logging_all.generate_gpu_index_price(
        gpu_name='H100',
        gpu_count=8,
        cpu_min=176, 
        cpu_max=256,  # removing outliers
        memory_min=1000, 
        memory_max=2048,
        removed_instances='pci',
        cpu_divisor=220,
        cpu_weighting=0.2,
        memory_divisor=1900,
        memory_weighting=0.1
    )
    print(h100_index_x8)

    Indices('H100_x1', current_time_nanos, h100_index_x1)
    Indices('H100_x8', current_time_nanos, h100_index_x8)

if __name__ == "__main__":
    main()
