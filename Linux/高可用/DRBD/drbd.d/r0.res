resource Mysqls {

  	meta-disk internal;
	
	disk {
		on-io-error detach;
	}
	
	startup { 
		degr-wfc-timeout 60;
	}
 
	on Mysql1 {
		device   /dev/drbd1;
		disk     /dev/sda1;
		address 10.0.0.7:7788;
	}
	on Mysql2 {
		device   /dev/drbd1;
		disk     /dev/sda1;
		address 10.0.0.8:7788;
	} 
}
