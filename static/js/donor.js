var app = angular.module('donorapp',['ngCookies','ngResource']);





app.factory('project',function ($resource){
	return $resource('/api/donorapp/project_and_scheme/',{},{
		getalldata:{method:'GET',params:{}}
 
	})

});
app.factory('pro',function ($resource){
	return $resource('/api/donorapp/show_donor_project/',{},{
		getalldata:{method:'GET',params:{}}
 
	})

});
app.factory('contribution',function ($resource){
	return $resource('/api/donorapp/my_contribution/',{},{
		getalldata:{method:'GET',params:{}}
 
	})

});
// app.factory('all_cont',function($resource){
// 	return $resource('/api/donorapp/show_dd_admin/',{},{
// 		getalldata:{method:'GET',params:{}}
// 	})

// });
// app.factory('acont_setng',function($resource){
// 	return $resource('/api/donorapp/account_setting/',{},{
// 		getalldata:{method:'GET',params:{}}
// 	})

// });

// app.factory('ds_status',function($resource){
// 	return $resource('/api/donorapp/donors_status/',{},{
// 		getalldata:{method:'GET',params:{}}
// 	})

// });



app.controller('donorappctrlr',function ($scope,$http,project,contribution,pro){

	$scope.project = function(){
		project.getalldata(function(response){
		$scope.project=response['project'];
		console.log(JSON.stringify($scope.project));

		});
	$scope.project_model=$scope.project[0];

	}
	$scope.project_model  
	
    $scope.age=function(){
    	$scope.age=[]
    	for(i=0;i<102;i++){
    		$scope.age.push(i);
            
    	}
    }
    $scope.achange=function(schemes_model){

    	if (schemes_model=='monthly'){
    		$scope.subscheme=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    	}
    	else if(schemes_model='yearly'){
    		var scheme = new Date().getFullYear()-20;
		    $scope.subscheme=[];
		    var a = 0;
		    for (var i = 0; i <= 40; i++) {
		    	$scope.subscheme.push(scheme+i);
		    };
    	}
    	else if(schemes_model='quarterly'){
    		$scope.subscheme=['q1','q2','q3','q4']
    	}
    }

	$scope.dnrs_status = function(project_model,schemes_model,sub_schemes_model){
		if (project_model==null){
			$scope.condition=''
            $scope.condition='Select Project';
            
		}
		else if(schemes_model==null){
			$scope.condition=''
            $scope.condition='Select Scheme';

		}
		else if(sub_schemes_model==null){
			$scope.condition=''
            $scope.condition='Select Sub Scheme';
		}
		else{
			$scope.condition=''
			var data={
			pro_model:project_model.project,
			sch_model:schemes_model,
			sub_sch_model:sub_schemes_model,
		    };
		    $http({
			    url:'/api/donorapp/donors_status/',
			    method:'POST',
			    data:data,
		    }).success(function(response){
			    // alert(JSON.stringify(response));
			    $scope.pendinguser=response['pendinguser'];
              
		});
	}
		
		
	}


	$scope.pro = function(){	
		pro.getalldata(function(response){
		$scope.projects=response['projects'];
		console.log(JSON.stringify($scope.projects));
		if ((JSON.stringify(response['projects'][0].schemes)) == '"monthly"'){
			$scope.schemes = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
		}
		else if ((JSON.stringify(response['projects'][0].schemes)) == '"yearly"'){
			var scheme = new Date().getFullYear()-20;
		    $scope.schemes=[];
		    var a = 0;
		    for (var i = 0; i <= 40; i++) {
		    	$scope.schemes.push(scheme+i);
		    };

		}
		else if ((JSON.stringify(response['projects'][0].schemes)) == '"quarterly"'){
			$scope.schemes = ['q1','q2','q3','q4'];

		}


		});
	}
	$scope.my_cont = function(){
		contribution.getalldata(function(response){
			$scope.my_contri = response['my_contribution']
		})
	}

	$scope.cont_details = function(){
		var data={
			key:'admin'
		};
		$http({
			url:'/api/donorapp/show_dd_admin/',
			method:'POST',
			data:data,
		}).success(function(response){
			$scope.cont_all= response['cont_all']
          
		});
		// all_cont.getalldata(function(response){
		// 	$scope.cont_all= response['cont_all']
		// })
   

	}
	$scope.add = function(new_pro,new_sch){
		var data = {
			anew_pro:new_pro,
			anew_sch:new_sch,
			key:'key',
		};
		$http({
			url:'http://10.0.1.32:8000/api/donorapp/project_and_scheme/',
			method:'POST',
			data:data,

		}).success(function(response){
			if(response.status = "saved"){
				alert("Saved Successfully!");
			    location.reload();

			}
  
		});

	};
	$scope.go = function(project_model,schemes_model){
		var data = {
			spro_model : project_model.project,
			ssch_model : schemes_model,
			cur_usr:'web',
			key : 'settings',
		};
		$http({
			url : 'http://10.0.1.32:8000/api/donorapp/project_and_scheme/',
			method : 'POST',
			data:data,
		}).success(function(response){
			if (response.status == "update"){
				alert('Change Project');
				window.location.href = '/donor/'

			}
			else if(response.status == "saved"){
                alert("Saved!")
                window.location.href = '/donor/'
			}

		});

	};
	$scope.change_pswd = function(username,epswd,repswd){
		if (username && epswd && repswd){
			if (epswd == repswd){
				var data = {
					cusername :username,
					cpswd :epswd,
				};
				$http({
					url: 'http://10.0.1.32:8000/api/donorapp/change_pswd/',
					data:data,
					method:'PATCH',
				}).success(function(response){
					if (response.status == "saved"){
						alert('Successfully changed your password');
						window.location.href = '/userlogin/'
					}
					else{
						alert('Username does not match');
					}

				});
			}
			else{
				alert('Password not match');
			}
		}
		else{
			alert('Fill All Fields');
		}
	}
	$scope.change_project = function(project_model,schemes_model){
		
		var data = {
			spro_model : project_model.project,
			ssch_model : schemes_model,
			usr:'web',
			key : 'change',
		};
		$http({
			url : 'http://10.0.1.32:8000/api/donorapp/project_and_scheme/',
			method : 'POST',
			data:data,
		}).success(function(response){
			// alert(JSON.stringify(response));
			if (response.amount !='0'){
				$scope.error_msg='"Already paid\u00A0'+response.amount+'.Rs for this month"';
			}
			else{
				$scope.error_msg = '';
			}

		});
	}
	$scope.delete = function(project_model,schemes_model){
		var data = {
			spro_model : project_model.project,
			ssch_model : schemes_model,
			key : 'delete'
		};
		$http({
			url : 'http://10.0.1.32:8000/api/donorapp/project_and_scheme/',
			method : 'POST',
			data:data,
		}).success(function(response){
			if (response.status == "deleted"){
				alert('Successfully deleted ');
			}

		});

	};
	$scope.acont_setting = function(){
		var data={
			key:'admin',
		};
		$http({
			url:'/api/donorapp/account_setting/',
			method:'POST',
			data:data
		}).success(function(response){
			$scope.sum=response['projects']

		});
		// acont_setng.getalldata(function(response){
			// alert(JSON.stringify(response));
			
		// })

	}

	$scope.login = function(username,password){
        var data = {
        	uname : username,
        	pswd : password,
        };

        
		$http({
			url:'http://10.0.1.32:8000/api/donorapp/donorlogin/',
			method:'POST',
			data:data,
		}).success(function(response){
			if(response.status == "success"){
				console.log(response);
				alert("welcome");
				window.location.href='/donor/'
			}
			else if(response.status == "admin"){
				window.location.href='/adminpage/'
				
			}
			else{
				alert("username or password is incorrect");
			}
		});
	};
	$scope.submit = function(project_model,schemes_model,amount){
		if(project_model && schemes_model && amount ){
			if(isNaN(amount)){
				alert('Amount should be number');
		}
		else{
			var data = {
			    dproject : project_model.project,
			    dscheme:schemes_model,
			    damount:amount,
			    cur_usr:'web',
			    
		   };
			
		}
			
			
	   }
		else{
			alert('Fill all field');
		}

		$http({
			url:'http://10.0.1.32:8000/api/donorapp/donate_detail/',
			method:'POST',
			data:data,

		}).success(function(response){
			if(response.status =="saved"){
				alert("Saved Successfully!");
				location.reload();
			}
          
		}); 
	}
	$scope.gender=["Male","Female"];
	$scope.save = function(username,gender_model,age,mail,number,address,pswd,rpswd){
		if (username && gender_model && age && mail && number && address && pswd && rpswd){
			if(pswd==rpswd){
				if(!isNaN(number)){
					var data = {
			            dusername:username,
                        dgender:gender_model,
			            dage:age,
			            dmail:mail,
			            dnumber:number,
			            daddress:address,
			            dpswd:pswd,
		            };
		            $http({
			            url:'http://10.0.1.32:8000/api/donorapp/user_register/',
			            method:'POST',
			            data:data,
		                }).success(function(response){
			                if(response.status == "saved"){
				                alert("Successfully Saved!");
				                window.location.href='/userlogin/';
			                 }
			                else if(response.status == "not"){
  				                	alert("username already registered");
			                  }

		                });
				}
				else{
					alert('Mobilenumber should be number');
				}
			
	        }
	        else{
	    	    alert("Password does not match");
	    }

		}
		else {
			alert('Fill All Fields');
		}

		
	}

});




// $scope.ds_status=response['paidscheme'];
// 		$scope.da =[];
// 		$scope.spl=[];
// 		// if (ds_status.scheme == 'Jan'||'Feb'||'Mar'||'Apr'||'May'||'Jun'||'Jul'||'Aug'||'Sep'||'Oct'||'Nov'||'Dec'){
// 		// 	$scope.user=response['paidscheme'][0].user;
// 		$scope.schemes = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
//         $scope.roles=[];
//         $scope.add =[];
// 		$scope.pending_schemes=$scope.schemes;
// 		console.log(JSON.stringify($scope.ds_status));
		
// 		for (var i=0;i<$scope.ds_status.length;i++) {
// 			alert($scope.ds_status.length);

// 			var pro=JSON.stringify($scope.ds_status[i]['project']);
// 			var sch = JSON.stringify($scope.ds_status[i]['scheme'])
// 			var usr = JSON.stringify($scope.ds_status[i]['user'])
// 			// console.log(pro,sch,usr);
// 			if (sch.indexOf($scope.schemes)){
// 			// if ((sch == '"Jan"')||(sch == '"Feb"')||(sch == '"Mar"')||(sch == '"Apr"')||(sch == '"May"')||(sch == '"Jun"')||(sch == '"Jul"')||(sch == '"Aug"')||(sch == '"Sep"')||(sch == '"Oct"')||(sch == '"Nov"')||(sch == '"Dec"')){
// 				    $scope.spl.push(sch);
// 				    alert($scope.spl);
// 				    $scope.schemes.splice($scope.schemes.indexOf($scope.spl), 1);
// 				    console.log(sch,pro,usr+"monthly");
			
//                     // $scope.add.push({sche: $scope.schemes, proje: pro,user:usr});
//                     // $scope.arr.push[{sche: sch, proje: pro,user:usr}];

// 			     }
// 			else if ((sch=='"q1"')||(sch=='"q2"')||(sch=='"q3"')||(sch=='"q4"')) {
// 				alert('ok');
// 				$scope.schemes=['q1','q2','q3','q4']
// 				$scope.spl.push(sch);
// 				$scope.schemes.splice($scope.schemes.indexOf($scope.spl), 1);
// 				// $scope.add.push({sche: $scope.schemes, proje: pro,user:usr});
// 				console.log(sch,pro,usr+"quarterly");
// 			}
// 			// else{
// 			// 	var sch = new Date().getFullYear()-20;
// 		 //        $scope.schemes=[];
// 		 //        var a = 0;
// 		 //        for (var i = 0; i <= 40; i++) {
// 		 //    	    $scope.schemes.push(sch+i);
// 		 //        };
// 		 //        $scope.schemes.splice($scope.schemes.indexOf(response['paidscheme'][i].scheme), 1);
// 		 //        console.log(sch,pro,usr+"yearly");
// 			// }
// 			$scope.add.push({sche: $scope.schemes, proje: pro,user:usr});
	
// 		}