USE [4Site]
GO

/****** Object:  Table [dbo].[tblQLPDUser]    Script Date: 17/06/2022 08:57:31 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tblQLPDUser](
	[UserID] [int] IDENTITY(1,1) NOT NULL,
	[Username] [nvarchar](50) NOT NULL,
	[Pwd] [nvarchar](250) NOT NULL,
	[PwdSalt] [nvarchar](150) NOT NULL,
	[DateCreated] [datetime] NOT NULL,
	[LastLogin] [datetime] NULL,
	[UserType] [int] NOT NULL,
 CONSTRAINT [PK_tblQLPDUser] PRIMARY KEY CLUSTERED 
(
	[UserID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


USE [4Site]
GO

/****** Object:  StoredProcedure [dbo].[spQLGetCaseNotes]    Script Date: 17/06/2022 08:58:42 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[spQLGetCaseNotes]
@clientID INT,
@strServiceString VARCHAR(100),
@groupString VARCHAR(100)

AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	CREATE TABLE #Srv(ServiceID INT)
	CREATE TABLE #Grp(GroupID INT)

	IF (@groupString = '' AND @strServiceString = '')
		BEGIN
			INSERT INTO #Grp SELECT tblService.GroupID FROM tblService
			INSERT INTO #Srv SELECT tblService.ServiceID FROM tblService
		END
	ELSE
		BEGIN
			IF (@groupString != '')
				BEGIN
					INSERT INTO #Grp SELECT * FROM fnCSVToTable(@groupString)
					INSERT INTO #Srv SELECT tblService.ServiceID FROM tblService
				END
			ELSE
				BEGIN
					INSERT INTO #Srv SELECT * FROM fnCSVToTable(@strServiceString)
					INSERT INTO #Grp SELECT tblService.GroupID FROM tblService
				END
		END
	
	SELECT DISTINCT
		SUBSTRING(tblClient.Firstname, 1, 1) + SUBSTRING(tblClient.Surname, 1, 1) Initials,
		tblCase.StartDate,
		tblCaseActivity.ActivityTime,
		tblCaseActivity.ActivityDate,
		CONVERT(NVARCHAR, tblCase.StartDate, 103) [CaseStartDate],
		tblService.Pneumonic [Service],
		tblCase.CaseID,
		CAST(tblCase.RefNumber AS INT) RefNo,
		CAST(tblCase.RefYear AS INT) RefYr,
		CONVERT(NVARCHAR, tblCaseActivity.ActivityDate, 103) [Date],
		CONVERT(NVARCHAR, tblCaseActivity.ActivityTime, 8) [Time],
		ISNULL(tblCaseNotesCategory.Narrative, tblQLActivityTypeRef.Narrative) + ISNULL(' - ' + tblCaseNotesSubCategory.Narrative, '') Activity,
		--tblCaseNotesCategory.Narrative CaseNotesCat,
		--ISNULL(tblCaseNotesSubCategory.Narrative, '') CaseNotesSubCat,
		--tblCaseActivity.Notes,
		--tblCaseActivity.Narrative,
		ISNULL(IIF(tblCaseActivity.Notes = '', tblCaseActivity.Narrative, tblCaseActivity.Notes), '') Notes

	FROM tblCase
		INNER JOIN tblClientCase ON tblCase.CaseID = tblClientCase.CaseID 
		INNER JOIN tblClient ON tblClientCase.ClientID = tblClient.ClientID
		INNER JOIN tblService ON tblCase.ServiceID = tblService.ServiceID 
		INNER JOIN tblServiceGroup ON tblService.GroupID = tblServiceGroup.ServiceGroupID
		INNER JOIN tblCaseActivity ON tblCase.CaseID = tblCaseActivity.CaseID
		LEFT JOIN tblCaseNotesCategory ON tblCaseActivity.CaseNotesCategoryID = tblCaseNotesCategory.CaseNotesCategoryID
		LEFT JOIN tblCaseNotesSubCategory ON tblCaseActivity.CaseNotesSubCategoryID = tblCaseNotesSubCategory.CaseNotesSubCategoryID
		LEFT JOIN tblSupportPlanCategory ON tblCaseActivity.CaseActivityID = tblSupportPlanCategory.CaseActivityID
		LEFT JOIN tblRiskAssessment ON tblCaseActivity.CaseActivityID = tblRiskAssessment.CaseActivityID
		LEFT JOIN tblRiskAssessmentStatus ON tblRiskAssessment.StatusID = tblRiskAssessmentStatus.RiskAssessmentStatusID
		LEFT JOIN tblQLActivityTypeRef ON tblCaseActivity.ActivityTypeID = tblQLActivityTypeRef.QLActivityTypeID
	WHERE
		tblClient.ClientID = @clientID
		AND tblCase.ServiceID IN (SELECT #Srv.ServiceID FROM #Srv)
		AND tblService.GroupID IN (SELECT #Grp.GroupID FROM #Grp)
	ORDER BY
		tblCase.StartDate, tblCaseActivity.ActivityDate, tblCaseActivity.ActivityTime ASC
	


	DROP TABLE #Srv
	DROP TABLE #Grp

END
GO


USE [4Site]
GO
/****** Object:  StoredProcedure [dbo].[spQLPDUserAdd]    Script Date: 17/06/2022 09:07:48 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[spQLPDUserAdd]
	@username NVARCHAR(50),
	@pwdHashStr NVARCHAR(250),
	@pwdSalt NVARCHAR(150),
	@usertype INT = 2
AS

	SET NOCOUNT ON;

	BEGIN TRANSACTION
		DECLARE @DateCreated DATETIME
		SET @DateCreated = GETDATE()

		INSERT INTO tblQLPDUser (Username, Pwd, PwdSalt, DateCreated, UserType)
		VALUES(@username, @pwdHashStr, @pwdSalt, @DateCreated, @usertype)
	COMMIT TRANSACTION
GO
/****** Object:  StoredProcedure [dbo].[spQLPDUserValidate]    Script Date: 17/06/2022 09:07:48 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[spQLPDUserValidate]
	-- Add the parameters for the stored procedure here
	@userID INT,
	@pwdHashStr NVARCHAR(150)
AS
BEGIN
	SET NOCOUNT ON;

    SELECT UserID FROM tblQLPDUser WHERE UserID = @userID AND Pwd = @pwdHashStr
END
GO
