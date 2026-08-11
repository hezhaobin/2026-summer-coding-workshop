angular.module("SignalP6", ['ngSanitize','rzModule', 'ui.bootstrap','chart.js']).config(function(){})



.controller("ResultsCtrl", ['$scope', '$http', '$uibModal', function($scope, $http, $uibModal) {

    $scope.outputActive = "showTpl"

    $scope.PDB = "";
    $scope.AdvancedOutput = "Off";
    $scope.advBtn = "danger"
    $scope.Error = false;

    $scope.jobid = getQueryParams(document.location.search).jobid;

    $scope.JSONLink = "/services/SignalP-6.0/tmp/" + $scope.jobid + "/output.json";;


    $scope.cf = function(focus) {
        if (!$scope.Error) {
            $scope.outputActive = focus
        }
    };
    
    $scope.open = function () {
        var modalInstance = $uibModal.open({
          templateUrl: 'thresholdGuide.html',
          controller: 'thrsguideController',
          size: 'wide',
        });

      };

    $scope.advancedOutputFunc = function () {
        if ($scope.AdvancedOutput == "Off"){
            $scope.AdvancedOutput = "On";
            $scope.advBtn = "success"
        } else {
            $scope.AdvancedOutput = "Off";
            $scope.advBtn = "danger"
        }
    }

    $scope.epiThreshold = {
        options: {
          ceil: 1,
          precision: 5,
          step: 0.01,
        }
    }
    // ----
    // Get the JSON results
    // ----

    $http.get($scope.JSONLink).success(function(response) {
        // Added optional key "Error" to JSON when python script logs an error message
        // If this key is there, show a different div that displays the traceback.
        $scope.JSON = response;

        if ($scope.JSON.hasOwnProperty('Error')){
            $scope.outputActive = "showTraceback";
            console.log('Found an Error message in response object, switch display mode.')
        }
        else{

        Object.keys($scope.JSON.antigens).forEach(function(key) {
            array = $scope.JSON.antigens[key].SS
            var returnarray = [];
            for(var i=0;i<array.length;i++){
              if(array[i] == 'H'){
                returnarray.push([array[i],'255,51,153'])
              } else if(array[i] == 'E'){ 
                returnarray.push([array[i],'51,153,204'])
              } else {
                returnarray.push([array[i],'255,153,51'])
              }
            }
            $scope.JSON.antigens[key].SS = returnarray
        })
        };
        console.log($scope.JSON)
        //when we get an error, there's no output file - we can only produce those from within the
        //code of the tool at the moment.
    }).error(function() {
        $scope.outputActive = "showLog";
        console.log('Got an error')
        $scope.Error = true;
    });
}])



.service('getBrowser', ['$window', function($window) {
        return function() {

            var userAgent = $window.navigator.userAgent;

            var browsers = {chrome: /chrome/i, safari: /safari/i, firefox: /firefox/i, msie: /msie/i, ie: /internet explorer/i};

            for(var key in browsers) {
                if (browsers[key].test(userAgent)) {
                    return key;
                }
           };

           return 'unknown';
        }

}])


.controller("InputCtrl", ['$scope', '$window', '$http', '$uibModal', 'getBrowser', function($scope, $window, $http, $uibModal, getBrowser) {
    $scope.fasta         = "";
    $scope.uploadfile    = "";
    $scope.fastafilename = "";
    $scope.organ         = "Eukarya";
    $scope.fmt           = "long"; 
    $scope.browser       = getBrowser($window);
    $scope.printme       = $window.navigator.userAgent;
    $scope.usBrowser = function () {
        if ($scope.browser == 'msie' || $scope.browser == 'ie'){
            return true
        } else if ($scope.browser == 'unknown') {
            return true
        } else {
            return false
        }
      };

    $scope.usBrowserOpen = function () {
        var modalInstance = $uibModal.open({
          templateUrl: 'usBrowser.html',
          controller: 'usBrowserController',
          size: 'wide',
        });

      };

    if ($scope.usBrowser() == true){
        $scope.usBrowserOpen()
    }

//    var defaultInputStatus = 'Input antigen sequence(s) in fasta format.';
//    $scope.inputStatus = defaultInputStatus;

//    $scope.open = function () {
//        var modalInstance = $uibModal.open({
//          templateUrl: 'thresholdGuide.html',
//          controller: 'thrsguideController',
//          size: 'wide',
//        });
//
//      };

    // console.log($scope.fastafilename)

    // $scope.invalidFastapaste = function() {return !$scope.fasta.match(/\>/gi)}
    // $scope.invalidFastafile = function() { return !$scope.fastafilename }
    
    // $scope.invalidForm = function() {
    //     if ($scope.invalidFastapaste() && $scope.invalidFastafile()) {
    //         $scope.inputStatus = defaultInputStatus;
    //         return true
    //     } else {
    //         $scope.inputStatus = "Ready to predict.";
    //         return false
    //     }
    // }

//    $scope.exclusionThreshold = {
//        value: 0.5,
//        options: {
//          ceil: 1,
//          precision: 5,
//          step: 0.01,
//        }
//    }

    $scope.resetall = function () {
        $scope.fasta = "";
        $scope.exclusionThreshold.value = 0.5;
        document.getElementById("uploadfile").value = null;
        document.getElementById("fastafileinfo").innerHTML = null;
    }

    $scope.loadExample = function() {
    	$scope.fasta = ">GLR1_DROME Glutamate receptor 1 OS=Drosophila melanogaster GN=GluRIA PE=1 SV=2\nMHSRLKFLAYLHFICASSIFWPEFSSAQQQQQTVSLTEKIPLGAIFEQGTDDVQSAFKYAMLNHNLNVSSRRFELQAYVDVINTADAFKLSRLICNQFSRGVYSMLGAVSPDSFDTLHSYSNTFQMPFVTPWFPEKVLAPSSGLLDFAISMRPDYHQAIIDTIQYYGWQSIIYLYDSHDGLLRLQQIYQELKPGNETFRVQMVKRIANVTMAIEFLHTLEDLGRFSKKRIVLDCPAEMAKEIIVQHVRDIKLGRRTYHYLLSGLVMDNHWPSDVVEFGAINITGFRIVDSNRRAVRDFHDSRKRLEPSGQSQSQNAGGPNSLPAISAQAALMYDAVFVLVEAFNRILRKKPDQFRSNHLQRRSHGGSSSSSATGTNESSALLDCNTSKGWVTPWEQGEKISRVLRKVEIDGLSGEIRFDEDGRRINYTLHVVEMSVNSTLQQVAEWRDDAGLLPLHSHNYASSSRSASASTGDYDRNHTYIVSSLLEEPYLSLKQYTYGESLVGNDRFEGYCKDLADMLAAQLGIKYEIRLVQDGNYGAENQYAPGGWDGMVGELIRKEADIAISAMTITAERERVIDFSKPFMTLGISIMIKKPVKQTPGVFSFLNPLSQEIWISVILSYVGVSFVLYFVTRFPPYEWRIVRRPQADSTAQQPPGIIGGATLSEPQAHVPPVPPNEFTMLNSFWYSLAAFMQQGCDITPPSIAGRIAAAVWWFFTIILISSYTANLAAFLTVERMVAPIKTPEDLTMQTDVNYGTLLYGSTWEFFRRSQIGLHNKMWEYMNANQHHSVHTYDEGIRRVRQSKGKYALLVESPKNEYVNARPPCDTMKVGRNIDTKGFGVATPIGSPLRKRLNEAVLTLKENGELLRIRNKWWFDKTECNLDQETSTPNELSLSNVAGIYYILIGGLLLAVIVAIMEFFCRNKTPQLKSPGSNGSAGGVPGMLASSTYQRDSLSDAIMHSQAKLAMQASSEYDERLVGVELASNVRYQYSM\n>CLV3_ARATH Protein CLAVATA 3 OS=Arabidopsis thaliana GN=CLV3 PE=1 SV=2\nMDSKSFLLLLLLFCFLFLHDASDLTQAHAHVQGLSNRKMMMMKMESEWVGANGEAEKAKTKGLGLHEELRTVPSGPDPLHHHVNPPRQPRNNFQLP\n>NAB2_SCHPO Nuclear polyadenylated RNA-binding protein nab2 OS=Schizosaccharomyces pombe (strain 972 / ATCC 24843) GN=nab2 PE=3 SV=1\nMTTLLETPGYSEKLHDSIEKKLSEYGWGEEAASLADFVLVMLSNGKTQTEINEELVDLIGSDFDTSFSLWLFNQIEELEKSKNASVESVSKIDEIDFIEKESTDKSQQSFSVPETSIQPQSSQTPNITSLREEKELPTGRVGQKLKLTSQKQRFNPMAASFNYSKSVMPAAKRALTQTQEVPLCKYADKCSRANCIFAHPTPAAAPGEGMVLSSEMCASGKECKAADCVKGHPSPATVTTLPPFMSMSTIPIPCKYKPCLNPACRFIHPTKSRNMTWRPPSKTEETSLSERSFAVNESEEQLHVPSV"
    }

}]);


function getQueryParams(qs) {
    qs = qs.split("+").join(" ");

    var params = {}, tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])]
            = decodeURIComponent(tokens[2]);
    }

    return params;
}
