import pandas as pd
import cv2


def ExtractData(LinkedInURL):
    #table = LinkedInURL
    # df = pd.read_csv("JobOp.csv")

    data = {'Job Title': ['Data Scientist', 'Software Engineer'],
            'Job Level': ['Entry', 'Experienced'],
            'Job Location': ['Bangalore', 'Bangalore'],
            'Salary': ['20 LPA', '10 LPA']
            }

    # Create DataFrame
    df = pd.DataFrame(data)

    for i in range(len(df.index)):
        JobTitle = df.iloc[i,0]
        JobLocation = df.iloc[i, 2]
        Salary = df.iloc[i,3]
        # Link = df.iloc[i, 5]
        return JobTitle, JobLocation, Salary


def FormatData(JobOp):
    Salary = JobOp[2]
    JobTitle = JobOp[0]
    JobLocation = JobOp[1]
    import cv2
    path = "PopUpBG.png"
    im = cv2.imread('PopUpBG.png', 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(im, Salary, (215, 100), font, 3, (0, 255, 0), 10, cv2.LINE_AA)
    cv2.putText(im, JobTitle, (70, 200), font, 3, (0, 0, 0), 10, cv2.LINE_AA)
    cv2.putText(im, JobLocation, (170, 540), font, 3, (0, 0, 0), 10, cv2.LINE_AA)
    cv2.imwrite('PopUpFinal1.jpg', im)
    # background = cv2.imread("PopUpBG.png", cv2.IMREAD_UNCHANGED)
    # foreground = cv2.imread("overlay.png", cv2.IMREAD_UNCHANGED)
    # alpha_background = background[:, :, 3] / 255.0
    # alpha_foreground = foreground[:, :, 3] / 255.0
    #
    # for color in range(0, 3):
    #     background[:, :, color] = alpha_foreground * foreground[:, :, color] + \
    #                               alpha_background * background[:, :, color] * (1 - alpha_foreground)
    #
    # # set adjusted alpha and denormalize back to 0-255
    # background[:, :, 3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255
    #
    # cv2.imshow("Composited image", background)
    # cv2.waitKey(0)
    return
def SendPopUp():
    pop = cv2.imread("PopUpFinal1.jpg")
    cv2.imshow('image', pop)
    cv2.waitKey(0)
    return
try:
    LinkedInURL=""
    CourseraURL = ""
    JobOp = ExtractData(LinkedInURL)
    # EduCo = ExtractData(CourseraURL)
    print(JobOp)

    JobOpFinal = FormatData(JobOp)
    # EduCoFinal = FormatData(EduCo)

    SendPopUp()
    # SendPopUp(EduCoFinal)
except Exception as e:
    print(e)