ALL: str = (
    "SELECT `a`.`DigitalDocID` AS 'Id' "
    "    , `b`.`Name` AS 'Folder' "
    "    , `a`.`DocDate` AS 'Date' "
    "    , `a`.`Author` AS 'Issuer' "
    "    , `a`.`DocTitle` AS 'Title' "
    "    , `c`.`ImagePosition` AS 'Page' "
    "    , `d`.`ImageId` AS 'ImageId' "
    "    , `d`.`ImageBytes` AS 'Image' "
    "FROM `DigitalDoc` `a` "
    "LEFT JOIN `Folder` `b` "
    "    ON `a`.`DigitalDocContainerID` = `b`.`ID` "
    "LEFT JOIN `DocImageLink` `c` "
    "    ON `a`.`DigitalDocID` = `c`.`DocId` "
    "LEFT JOIN `Images` `d` "
    "    ON `c`.`ImageId` = `d`.`ImageId` "
    "WHERE `a`.`Deleted` = 0 "
    "    AND `a`.`DocDate` IS NOT NULL "
    "    AND `a`.`DocTitle` IS NOT NULL "
    "ORDER BY `Id`, `Page`"
)

DOCUMENTS: str = (
    "SELECT `a`.`DigitalDocID` AS 'Id' "
    "    , `a`.`DocDate` AS 'Date' "
    "    , `a`.`Author` AS 'Author' "
    "    , `a`.`DocTitle` AS 'Title' "
    "    , `b`.`Name` AS 'Folder' "
    "FROM `DigitalDoc` `a` "
    "LEFT JOIN `Folder` `b` "
    "    ON `a`.`DigitalDocContainerID` = `b`.`ID` "
    "WHERE `a`.`Deleted` = 0"
)

RECEIPTS: str = (
    "SELECT `a`.`FinancialDocId` AS 'Id' "
    "    , `a`.`DocDate` AS 'Date' "
    "    , `b`.`vendorName` AS 'Author' "
    "    , `b`.`TotalAmount` AS 'Title' "
    "    , `c`.`Name` AS 'Folder' "
    "FROM `FinancialDoc` `a` "
    "LEFT JOIN `FinancialDocLineItem` `b` "
    "    ON `a`.`FinancialDocId` = `b`.`FinancialDocId` "
    "LEFT JOIN `Folder` `c` "
    "    ON `a`.`FinancialContainerId` = `c`.`ID` "
    "WHERE `a`.`Deleted` = 0"
)

IMAGES: str = (
    "SELECT `b`.`ImageId` AS 'ImageId' "
    "    , `b`.`ImageBytes` AS 'Image' "
    "FROM `DocImageLink` `a` "
    "LEFT JOIN `Images` `b` "
    "    ON `a`.`ImageId` = `b`.`ImageId` "
    "WHERE `a`.`DocId` = ? "
    "ORDER BY `a`.`ImagePosition`"
)