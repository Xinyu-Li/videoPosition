import cv2

def draw_main_locations(frame):
    """---------------------------------基准线------------------------------------------"""

    # cv2.line(frame, (10, line_height), (1200, line_height), (255, 255, 0), 3)
    # cv2.line(frame, (1180, 10), (1180, 710), (255, 255, 0), 3)
    # cv2.line(frame, (1, 1), (1180, 1), (255, 255, 0), 3)

    """---------------------------------画出主要标识点-------------------------------"""
    # Floor plan, 7057, 9464  # 整个场地大小，长和宽

    # Phone, 2886, 9283
    cv2.putText(frame, "phone", (1100, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.circle(frame, (1120, 360), 5, color=[0, 255, 255], thickness=-1)
    # ECG, 6542, 5988
    cv2.putText(frame, "ECG", (650, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.circle(frame, (670, 420), 5, color=[0, 255, 255], thickness=-1)
    # Meds, 6442, 5018
    cv2.putText(frame, "Meds", (720, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.circle(frame, (740, 380), 5, color=[0, 255, 255], thickness=-1)

    """---------------------------------------------------------------------------------------------------"""
    # B1 laptop, 4564, 7589
    cv2.putText(frame, "B1 lp", (965, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (159, 255, 84), 2)
    cv2.circle(frame, (965, 400), 5, color=[159, 255, 84], thickness=-1)
    # B1 centre, 5496, 7589
    # B1 monitor, 6820, 6820
    cv2.putText(frame, "B1 mo", (1210, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (159, 255, 84), 2)
    cv2.circle(frame, (1250, 440), 5, color=[159, 255, 84], thickness=-1)
    # B1 oxygen, 6781, 8336
    """cannot see"""
    # B1 patient, 5911, 7589
    cv2.putText(frame, "B1 pa", (1120, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (159, 255, 84), 2)
    cv2.circle(frame, (1120, 450), 5, color=[159, 255, 84], thickness=-1)

    """---------------------------------------------------------------------------------------------------"""
    # B2 laptop, 2478, 6581
    cv2.putText(frame, "B2 lp", (420, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 32, 160), 2)
    cv2.circle(frame, (420, 420), 5, color=[240, 32, 160], thickness=-1)
    # B2 centre, 1547, 6581
    # B2 monitor, 223, 5834
    cv2.putText(frame, "B2 mo", (80, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 32, 160), 2)
    cv2.circle(frame, (80, 400), 5, color=[240, 32, 160], thickness=-1)
    # B2 oxygen, 292, 7358
    cv2.putText(frame, "B2 ox", (10, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 32, 160), 2)
    cv2.circle(frame, (10, 330), 5, color=[240, 32, 160], thickness=-1)
    # B2 patient, 1124, 6581
    cv2.putText(frame, "B2 pa", (200, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 32, 160), 2)
    cv2.circle(frame, (200, 470), 5, color=[240, 32, 160], thickness=-1)

    """---------------------------------------------------------------------------------------------------"""
    # B3 laptop, 4564, 3156
    cv2.putText(frame, "B3 lp", (560, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 118, 72), 2)
    cv2.circle(frame, (565, 370), 5, color=[255, 118, 72], thickness=-1)
    # B3 centre, 5480, 3156
    # B3 monitor, 6827, 2371
    cv2.putText(frame, "B3 mo", (550, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 118, 72), 2)
    cv2.circle(frame, (570, 310), 5, color=[255, 118, 72], thickness=-1)
    # B3 oxygen, 6827, 3895
    cv2.putText(frame, "B3 ox", (635, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 118, 72), 2)
    cv2.circle(frame, (635, 310), 5, color=[255, 118, 72], thickness=-1)
    # B3 patient, 5911, 3156
    cv2.putText(frame, "B3 pa", (580, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 118, 72), 2)
    cv2.circle(frame, (580, 345), 5, color=[255, 118, 72], thickness=-1)

    """---------------------------------------------------------------------------------------------------"""
    # B4 laptop, 2478, 2802
    cv2.putText(frame, "B4 lp", (920, 345), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 187, 255), 2)
    cv2.circle(frame, (920, 365), 5, color=[255, 187, 255], thickness=-1)
    # B4 centre, 1539, 2802
    # B4 monitor, 223, 2047
    cv2.putText(frame, "B4 mo", (810, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 187, 255), 2)
    cv2.circle(frame, (830, 315), 5, color=[255, 187, 255], thickness=-1)
    # B4 oxygen, 285, 3541
    cv2.putText(frame, "B4 ox", (880, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 187, 255), 2)
    cv2.circle(frame, (880, 320), 5, color=[255, 187, 255], thickness=-1)
    # B4 patient, 1293, 2802
    cv2.putText(frame, "B4 pa", (850, 345), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 187, 255), 2)
    cv2.circle(frame, (870, 365), 5, color=[255, 187, 255], thickness=-1)

    # Equip left, 1155, 292
    cv2.putText(frame, "Eq left", (410, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 50), 2)
    cv2.circle(frame, (410, 350), 5, color=[255, 255, 50], thickness=-1)
    # Equip right, 5819, 292
    cv2.putText(frame, "Eq right", (130, 365), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 50), 2)
    cv2.circle(frame, (130, 385), 5, color=[255, 255, 50], thickness=-1)

    """---------------------------------------------------------------------------"""


