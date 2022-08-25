Script allows user to list BLOBs in storege account container and download certain BLOBs.
To run:
1. Copy connection string. See the [Manage storage account access keys article ](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys)
2. (if you plan to test BLOBs download) Create "dl.txt" file in the same directory
3. Execute script using python and pass conenction string as the only argument to this script, e.g. `python main.py "DefaultEndpointsProtocol=https;AccountName=username;AccountKey=xxx;EndpointSuffix=core.windows.net"`
4. Script displays all the BLOBs found in all containers in provided (via connection string) storage account
5. (if you plan to save BLOBs listing) Type "y" when prompted "Do you need to save listing of BLOBs (y/n): "
6. Type file name when prompted "Specify file name to save this output: "
7. Confirm file is created and it lists all BLOBs as expected
8. (if you plan to download BLOBs) Type "y" when prompted "Do you need to download BLOBs (y/n): "
9. Script reads content of "dl.txt" file and downloads all BLOBs specified. Example "dl.txt" file is below: 
    ```
    Veeam/Backup365/vbm-cold-folder/CommonInfo/RepositoryConfig.0000001A
    Veeam/Backup365/vbm-folder/Organizations/d8b2921f42d445ed80a5075d57421a44/Webs/fe844d0b95874e019bdcc66d95e18ba0/ListsData/2e74cefd6e5544efbb3ac1371f9adfc9.0000000E
    Veeam/Backup365/vbm-folder/Organizations/d8b2921f42d445ed80a5075d57421a44/Webs/fe844d0b95874e019bdcc66d95e18ba0/Items/f3da2af3c4b245648da85c37fb94e574/988a1b0122c2473a9fbdef782eee1ead.77c03eafef33422991d1d8f27d5f4557
    ```
10. Confirm specified BLOBs are downloaded
