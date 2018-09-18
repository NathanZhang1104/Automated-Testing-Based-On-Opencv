
import time
import wmi
start=time.time()
def T(s=-1):
    ret=time.time()-start
    if s!=-1:
        s2=str(time.time()-start)
        s=str(s)
        print(s+':'+s2)
    return ret
def get_cpu_info():
    tmpdict = {}
    tmpdict["CpuCores"] = 0
    c = wmi.WMI()
    c.Win32_Processor()

    for cpu in c.Win32_Processor():
        #                print cpu
        print("cpu id:", cpu.ProcessorId.strip())
        tmpdict["CpuType"] = cpu.Name
        ret=cpu.ProcessorId.strip()
        try:
            tmpdict["CpuCores"] = cpu.NumberOfCores
        except:
            tmpdict["CpuCores"] += 1
            tmpdict["CpuClock"] = cpu.MaxClockSpeed
            return tmpdict
    return ret


def _read_cpu_usage():
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        return cpu.LoadPercentage


def get_cpu_usage():
    cpustr1 = _read_cpu_usage()
    if not cpustr1:
        return 0
    time.sleep(2)
    cpustr2 = _read_cpu_usage()
    if not cpustr2:
        return 0
    cpuper = int(cpustr1) + int(cpustr2) / 2
    return cpuper


def get_disk_info():
    tmplist = []
    encrypt_str = ""
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        # cpu 序列号
        encrypt_str = encrypt_str + cpu.ProcessorId.strip()
        print("cpu id:", cpu.ProcessorId.strip())
    for physical_disk in c.Win32_DiskDrive():
        encrypt_str = encrypt_str + physical_disk.SerialNumber.strip()

        # 硬盘序列号
        print('disk id:', physical_disk.SerialNumber.strip())
        tmpdict = {}
        tmpdict["Caption"] = physical_disk.Caption
        tmpdict["Size"] = len(physical_disk.Size) / 1000 / 1000 / 1000
        tmplist.append(tmpdict)
    for board_id in c.Win32_BaseBoard():
        # 主板序列号
        encrypt_str = encrypt_str + board_id.SerialNumber.strip()
        print("main board id:", board_id.SerialNumber.strip())
    #          for mac in c.Win32_NetworkAdapter():

    # mac 地址（包括虚拟机的）
    #                    print "mac addr:", mac.MACAddress:
    for bios_id in c.Win32_BIOS():
        # bios 序列号
        encrypt_str = encrypt_str + bios_id.SerialNumber.strip()
        print("bios number:", bios_id.SerialNumber.strip())
    print("encrypt_str:", encrypt_str)

    # 加密算法
    # print(zlib.adler32(encrypt_str))
    return encrypt_str


def encryption(str):
    en_list=[]
    for i in range(len(str)):
        en_list.append(ord(str[i]))
    k=1
    for i in range(len(en_list)):
        k+=en_list[i]*(1104+i*981104)
    return k
def check(encry,password):
    print(encryption(encry),password)
    if encryption(encry)==password:
        ret=True
    else:
        ret=False
    return ret
if __name__ == "__main__":
    #     a = get_cpu_info()
    # a=get_disk_info()
    # print(a)
    T(0)
    a=get_cpu_info()
    T(1)
    password=encryption('BFEBFBFF000206D7')

    print(password)