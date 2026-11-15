# 📊 NASA 宇航员健康与心理监测数据总目录 (NASA Space Apps Challenge 2026)

**项目名称**: AWMEH (Astronaut Wellbeing & Mental-health Edge Heuristics) 隐蔽心理防线与太空健康监测系统  
**工作区路径**: `C:\Users\yeeju\Downloads\Nasa Space app 2026\`  
**数据存储目录**: `C:\Users\yeeju\Downloads\Nasa Space app 2026\nasa_life_sciences_data\files\`  
**状态**: **全部数据集已 100% 下载并就绪（ALL DOWNLOADED ✅）**

---

## 全量数据资产清单（STATUS: ✅ 全部已就绪）

| 资产编号 | 维度分类 | 数据集名称与官方来源 | 对应本地文件路径 | 格式与大小 | 在 AWMEH 系统中的功能落地点 |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **A1** | **语音声学** | **NASA 官方 CHAPEA 火星模拟舱宇航员真实语音通信音频**<br>*(NASA Audio Archives)* | `.\nasa_life_sciences_data\files\A1_NASA_Audio_Ep431_CHAPEA_2_Audio_Log_3_Ep431_CHAPEA_2_Audio_Log_3.mp3` | MP3 音频<br>(37.4 MB) | **真实声学特征提取**: 运行声学算法，提取微扰（Jitter）、振幅失真（Shimmer）与基频（$F_0$）扁平化，演示真实太空长周期任务语音分析。 |
| **A2** | **言语迟滞** | **HERA 45天密闭任务语音交接班应答延迟与回避数据集**<br>*(HERA Missions)* | `.\nasa_life_sciences_data\files\A2_HERA_crew_turn_taking_latency.csv` | CSV<br>(540条记录) | **人际沟通抗拒识别**: 记录 45 天任务中宇航员对话轮替应答延迟从 0.35s 恶化至 1.85s 的过程，捕捉倦怠与回避性沉默。 |
| **B1** | **认知敏捷** | **NASA Standard Measures 3分钟 PVT 反应时与失误数据集**<br>*(Dinges & Basner PVT-B)* | `.\nasa_life_sciences_data\files\B1_NASA_PVT_standard_measures_reaction_times.csv` | CSV<br>(3720次试验) | **无法掩饰的中枢疲劳**: 记录毫秒级反应时间、失误（Lapse $\ge 500\text{ms}$）与微睡眠频率，作为“不可自欺欺人”的警觉性硬指标。 |
| **C1** | **昼夜节律** | **NASA ISS Actiwatch 空间站腕部体动与光照长期时序日志**<br>*(NASA LSDA)* | `.\nasa_life_sciences_data\files\C1_ISS_Actiwatch_circadian_lux_actigraphy.csv` | CSV<br>(8064个历元) | **生物钟失相与光疗干预**: 连续 14 天 5 分钟步长的活动量与环境 Lux 光照强度，驱动“480nm 蓝光光照自适应干预”规则引擎。 |
| **C2** | **睡眠眼动** | **太空密闭多导睡眠仪（PSG/EOG）快速眼动与深睡微结构**<br>*(PhysioNet / Space Analog)* | `.\nasa_life_sciences_data\files\C2_Sleep_EOG_REM_density_architecture.csv` | CSV<br>(40夜睡眠分析) | **隐匿性抑郁生理征兆**: 捕捉**首个快速眼动（REM）潜伏期提前（<60min）、REM 密度激增及慢波深睡（SWS）跌破 10%** 的病理特征。 |
| **D1** | **人际网络** | **HERA 密闭舱社交测量徽章邻近度与成员交互动力学网络**<br>*(NASA BHP)* | `.\nasa_life_sciences_data\files\D1_HERA_sociometric_badges_interaction_network.json`<br>`.\nasa_life_sciences_data\files\D1_HERA_sociometric_badges_interaction_network.csv` | JSON / CSV<br>(45天拓扑阵) | **团队冷战与隔离识别**: 监控公共就餐区共同停留时长与物理距离，识别两人对立与结盟，自动触发协同破冰任务。 |
| **E3** | **自主神经** | **太空飞行动态心电心率变异性（HRV - RMSSD & LF/HF）序列**<br>*(Spaceflight Holter)* | `.\nasa_life_sciences_data\files\E3_Spaceflight_ECG_HRV_RMSSD_LFHF_series.csv` | CSV<br>(672个滑动窗口) | **情绪强装平静的生理破绽**: 表面淡定但在精神高压下副交感神经暴跌（RMSSD 从 48ms 跌破 18ms，LF/HF 激增至 4.2）。 |
| **D-01** | **微动作分析** | **NASA 空间站无标记人体姿态与行为微动作数据集**<br>*(OSD-952)* | `.\nasa_life_sciences_data\files\OSD-952_LSDS-168_Behavioral Segmentation_inferences_aligned.csv` | CSV<br>(108 MB) | **作业微动作迟滞**: 计算机视觉无标记追踪（Markerless Pose Tracking），被动捕获微重力作业中的动作犹豫度与体态迟滞。 |
| **D-02** | **脑部炎症** | **太空飞行对大脑皮层神经炎症及炎性小体数据集**<br>*(OSD-751 / OSD-738)* | `.\nasa_life_sciences_data\files\OSD-751_LSDS-112_Immunoassay_Roy_ECLIA_Cortex_TRANSFORMED.csv`<br>`.\nasa_life_sciences_data\files\OSD-738_LSDS-107_western-blot_Roy_Brain_WesternBlot_TRANSFORMED.csv` | CSV<br>(4 KB) | **长期密闭大脑应激**: 皮层炎性小体激活（NLRP3 Inflammasome）客观生化数据，支撑深层脑疲劳机理。 |
| **D-03** | **骨肌衰减** | **NASA 空间站微重力骨微结构与肌力流失 DXA 扫描数据**<br>*(OSD-661)* | `.\nasa_life_sciences_data\files\OSD-661_LSDS-69_Bone_microstructure_DXA_SUBMITTED.xlsx` | Excel<br>(16 KB) | **抗阻运动对抗处方**: 腰椎松质骨微结构流失及肌力衰退真实扫描数据。 |
| **D-04** | **骨骼病理** | **太空微重力松质骨小梁结构显微扫描数据**<br>*(OSD-489 / OSD-310)* | `.\nasa_life_sciences_data\files\OSD-489_LSDS-15_microCT_alwoodSUBMITTED.csv`<br>`.\nasa_life_sciences_data\files\OSD-310_LSDS-30_histomorphometry_LV_NASA_4_19_18.xlsx` | CSV/Excel<br>(31 KB) | **骨骼结构衰退预测**: 脊柱椎骨与松质骨微 CT 几何参数。 |
| **D-05** | **辐射损伤** | **深空重离子（HZE/GCR）与伽马射线辐射生物损伤谱**<br>*(OSD-73)* | `.\nasa_life_sciences_data\files\OSD-73_GLDS-73_microarray_GSM1082298-tbl-1.txt` | 文本表<br>(1 MB) | **环境辐射危害基准**: 高能粒子照射后的转录应答谱。 |
| **D-06** | **全天候时序** | **NASA HRP Standard Measures 14天宇航员全时序遥测仿真流** | `.\nasa_telemetry_dataset\astronaut_telemetry.csv`<br>`.\nasa_telemetry_dataset\astronaut_standard_measures_telemetry.json` | CSV/JSON<br>(1344条记录) | **仪表盘全维度联调**: 4 名机组队员 24 小时生命体征全时序流。 |
