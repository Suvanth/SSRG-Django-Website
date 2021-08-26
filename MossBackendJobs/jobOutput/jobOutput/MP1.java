import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class MarketPlace{
   public static void main(final String[] args) throws FileNotFoundException{
   Currency rand = new Currency("R", "ZAR", 100); // currency used for the money object
   String Product=""; // var used to store the users input for product eg. lettuce
   int iCount = 0; // used for index of the array
   int NumUnits =0; // var used to store the users input for num of units required 
   int FirstElement=0;

   int iElements=0;
   int iNumMatches=0;
   Scanner in = new Scanner(System.in);
   System.out.println("Enter the name of a \"Comma Separated Values\" (CSV) file:") ;
   String fileName = in.nextLine();//gets filename from user
   File file = new File(fileName);
   if (file.length()>0){
   Scanner fileInput = new Scanner(new File(fileName));
   FirstElement = Integer.valueOf(fileInput.nextLine());
   }
   if ((file.length()==0)||(FirstElement==0)) {
   System.out.println("The file contains no seller data.");       // checks that the file is empty
   } else{                                                      
   Scanner fileIn = new Scanner(new File(fileName));
   iElements = Integer.valueOf(fileIn.nextLine());
   Seller [] records;
   records = new Seller[iElements];
   String firstLine = fileIn.nextLine();
   
   while (fileIn.hasNextLine()) {
   firstLine = fileIn.nextLine();
   Scanner scanner = new Scanner(firstLine); //**problem
   scanner.useDelimiter("\\s*,\\s*");
   Seller seller_record = new  Seller();
   seller_record.ID = scanner.next();
   seller_record.name = scanner.next();
   seller_record.location = scanner.next();
   seller_record.product = scanner.next();
   Money unit_record = new Money(scanner.next(), rand);
   seller_record.unit_price = unit_record;
   seller_record.number_of_units = Integer.valueOf(scanner.next());
   records[iCount] = seller_record;
   iCount = iCount+1;   
   }
   System.out.println("Enter the name of a product:");
   Product = in.nextLine();
   System.out.println("Enter the number of units required:");
   NumUnits = Integer.valueOf(in.nextLine());
   System.out.println("Enter the maximum unit price:");
   Money money1 = new Money(in.nextLine(),rand);
   for (int i = 0; i < iElements-1; i++) {
   int Comp = money1.compareTo(records[i].unit_price);
   if ( (Product.equals(records[i].product)) && (records[i].number_of_units>=NumUnits) && (Comp>-1) ){
   System.out.println(records[i].ID+" : "+records[i].name+" in "+records[i].location+" has "+records[i].number_of_units+" "+Product+" for "+records[i].unit_price+" each.");
   iNumMatches=iNumMatches+1;   
   }





}
if (iNumMatches==0){
System.out.println("None found.");
}



   
   }
   
 }  

   }