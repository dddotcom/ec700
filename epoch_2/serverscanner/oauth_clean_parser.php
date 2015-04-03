<?php

//make sure any errors that occur including server errors are displayed

ini_set('display_errors', 1);

// Create a DOM parser object
$dom = new DOMDocument();
//load contents from web crawler (html version)
$html =file_get_contents("delta.html");

@$dom->loadHTML($html);
$javascript=0;
$secure=0;
$vulnerable=0;
$total=0;
$uncategorized=0;

echo "<table border=1><tr><td width=70px>website</td><td>-</td></tr>";

// Iterate over all the <a> tags
foreach($dom->getElementsByTagName('a') as $link) {
        //create the link to the page found by crawler and create a DOM object for that too
	$urlInner = $link->getAttribute('href');
//	echo "<tr><td> ".$urlInner."</td><td><table style=border:1px;><tr><td>href</td><td>data-url</td><td>text value</td><td>Secure?</td></tr> ";
	$domInner = new DOMDocument();
	$htmlInner = file_get_contents($urlInner);
	@$domInner->loadHTML($htmlInner);
	$search_text="FACEBOOK";
	$total=$total+1;
	//find facebook
	foreach($domInner->getElementsByTagName('a') as $linkInner) {
        if (strpos(strtoupper($linkInner->getAttribute('href')), $search_text) ||strpos(strtoupper($linkInner->getAttribute('data_url')), $search_text)||strpos(strtoupper($linkInner->nodeValue), $search_text))
	{
		//check if the link uses javascript
		if(strpos($linkInner->getAttribute('href'), "#")!==false ||strpos($linkInner->getAttribute('data_url'), "#")!==false||strpos($linkInner->nodeValue,"#")!==false||strpos($linkInner->getAttribute('href'), "javascript")!==false ||strpos($linkInner->getAttribute('data_url'), "javascript")!==false||strpos($linkInner->nodeValue,"javascript")!==false)
		{
			//if it does add to output
			echo "<tr>";
        		echo "<td> ".$urlInner."</td>";

			echo "<td> Javascript </td> ";
        		echo "</tr>";
			$javascript=$javascript+1;
		}
		else
		{
			//assume serverside
			//not using javascript
			if(strpos($linkInner->nodeValue,"using")!==false||strpos($linkInner->nodeValue,"with")!==false||strpos(strtoupper($linkInner->getAttribute('href')), "AUTH")!==false||strpos(strtoupper($linkInner->getAttribute('href')), "SIGNIN")!==false ) 
			{
			
				echo "<tr> ";
				echo "<td> ".$urlInner."</td>";

				if((strpos($linkInner->getAttribute('href'), "response_type")!==false||strpos($linkInner->getAttribute('href'), "token")!==false)&&strpos($linkInner->getAttribute('href'), "oauth")!==false)
				{
					echo "<td><font color=red>Vulnerable</font></td> ";
					$vulnerable=$vulnerable+1;
				}
				elseif(strpos($linkInner->getAttribute('href'), "facebook")===false)
				{
					echo "<td><font color=red>Vulnerable</font></td> ";

					$vulnerable=$vulnerable+1;
				}
				else
				{
					echo "<td><font color=green>Secure</font></td>";
					$secure=$secure+1;
				}
                		echo "</tr>";
			//	$count=$count+1;
			} 
		}
	}
 	else
        {
                $uncategorized=$uncategorized+1;
        }
	}
}
echo "</table>";
echo "<br/><br/><br/>";
echo "Total Number of sites: ".$total." <br/>";
echo "Total Number of sites using javascript: ".$javascript."<br/>";
echo "Total Number of vulnerable sites: ".$vulnerable." <br/>";
echo "Total Number of secure sites: ".$secure." <br/>";
//echo "Total Number of uncategorized sites: ".$uncategorized." <br/>";

?>
