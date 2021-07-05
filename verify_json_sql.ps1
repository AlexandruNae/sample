[string]$ServerInstance = "mydatasource,port#"
[string]$Database = "mydatabasename"
[string]$Query ="select * from Types"
[Int32]$QueryTimeout=30

$conn = New-Object System.Data.Odbc.OdbcConnection
    $conn.ConnectionString="dsn=mirror_live;"
    $conn.open()
   



$judete = @('ALBA','ARAD','ARGES','BACAU','BIHOR','BISTRITA-NASAUD','BOTOSANI','BRASOV','BRAILA','BUCURESTI','BUZAU','CARAS-SEVERIN','CALARASI','CLUJ','CONSTANTA','COVASNA','DAMBOVITA','DOLJ','GALATI','GIURGIU','GORJ','HARGHITA','HUNEDOARA','IALOMITA','IASI','ILFOV','MARAMURES','MEHEDINTI','MURES','NEAMT','OLT','PRAHOVA','SATU MARE','SALAJ','SIBIU','SUCEAVA','TELEORMAN','TIMIS','TULCEA','VASLUI','VALCEA','VRANCEA','SEVERIN','BISTRITA','CARAS')

$dict = New-Object 'system.collections.generic.dictionary[string,string]'
    $dict["RO15710936"] = "AVA"
    $dict["15710936"] = "AVA"

    $dict["RO18463202"] = "CMBC"
    $dict["18463202"] = "CMBC"

    $dict["RO5919324"] = "CMU"
    $dict["5919324"] = "CMU"

    $dict["RO18463202"] = "CMUCJ"
    $dict["18463202"] = "CMUCJ"

    $dict["RO14009050"] = "ECH"
    $dict["14009050"] = "ECH"

    $dict["RO27590027"] = "EFORA"
    $dict["27590027"] = "EFORA"

    $dict["RO14105023"] = "EMC"
    $dict["14105023"] = "EMC"

    $dict["RO29410661"] = "GASTRO"
    $dict["29410661"] = "GASTRO"

    $dict["RO33370956"] = "HISTRIA"
    $dict["33370956"] = "HISTRIA"

    $dict["RO28353290"] = "MSM"
    $dict["28353290"] = "MSM"

    $dict["RO26630352"] = "POND"
    $dict["26630352"] = "POND"

    $dict["RO2610501"] = "PULS"
    $dict["2610501"] = "PULS"

    $dict["RO16491486"] = "PURG"
    $dict["16491486"] = "PURG"

    $dict["RO24454900"] = "SANT"
    $dict["24454900"] = "SANT"

    $dict["RO24469080"] = "STEM"
    $dict["24469080"] = "STEM"

    $dict["RO29114763"] = "PHOENIX"
    $dict["29114763"] = "PHOENIX"

    $dict["RO18164472"] = "ELITE"
    $dict["18164472"] = "ELITE"

    $dict["RO22183847"] = "POZIMED"
    $dict["22183847"] = "POZIMED"

    $dict["19216537"] = "CRB"
    $dict["RO19216537"] = "CRB"

    $dict["RO25109543"] = "GENETIC"
    $dict["25109543"] = "GENETIC"

    $dict["RO35621094"] = "GENOME"
    $dict["35621094"] = "GENOME"

    $dict["RO22355713"] = "BIOST2007"
    $dict["22355713"] = "BIOST2007"

    $dict["RO17002740"] = "BIOST"
    $dict["17002740"] = "BIOST"

    $dict["RO29290603"] = "PREM"
    $dict["29290603"] = "PREM"

    $dict["RO30157091"] = "SOMESAN"
    $dict["30157091"] = "SOMESAN"


$ignore_data = $false

$today = Get-Date 


$dict_luna = New-Object 'system.collections.generic.dictionary[string,string]'
$dict_luna["1"] = "ianuarie"
$dict_luna["2"] = "februarie"
$dict_luna["3"] = "martie"
$dict_luna["4"] = "aprilie"
$dict_luna["5"] = "mai"
$dict_luna["6"] = "iunie"
$dict_luna["7"] = "iulie"
$dict_luna["8"] = "august"
$dict_luna["9"] = "septembrie"
$dict_luna["10"] = "octombrie"
$dict_luna["11"] = "noiembrie"
$dict_luna["12"] = "decembrie"

$folder = [string]$today.Year + "\" + $dict_luna[[string]$today.Month] + "\" + [string]$today.Day
#$folder = [string]$today.Year + "\" + $dict_luna[[string]$today.Month] + "\test6"


$today = Get-Date -format dd/MM/yyyy 



$validate_error ='C:\Users\quasar\invoice_handling\'+$folder+'\4_VALIDATE_ERROR\'
$validate_invoice ='C:\Users\quasar\invoice_handling\'+$folder+'\5_VALIDATE_INVOICE\'
$dir_plm='C:\Users\quasar\invoice_handling\'+$folder+'\6_FILL_PLM\'
$dir_plm_error='C:\Users\quasar\invoice_handling\'+$folder+'\7_FILL_PLM_ERROR\'
$procesate = 'C:\Users\quasar\invoice_handling\'+$folder+'\3.1_procesate\'
$invoice_json = 'C:\Users\quasar\invoice_handling\'+$folder+'\3.0_INVOICE_JSON'
$files = Get-ChildItem $invoice_json
#citire json
$count = 1
#$files = Get-ChildItem "C:\Users\quasar\invoice_handling\INVOICE_JSON\"

foreach ($f in $files){
    
    $nume_reprezentant = ''

    $outfile = $f.FullName 
    $reason = ""
    $validate = $true
    $suma_afisat = ''

    $name = $f.Name
    #    Where-Object { $_.LastWriteTime -gt [DateTime] $filesNewerThan } |
    $filePath = $f.FullName
    $data = Get-ChildItem -File $filePath -Recurse | ForEach-Object {
                Get-Content -Raw -LiteralPath $_.FullName | ConvertFrom-Json 
            }


    $cui_factura = $data.Furnizor.cod
    $cui_client = $data.Client.cod
    $cont_factura = $data.Furnizor.IBAN
    $suma_factura = $data.total
    #if($suma_factura -match ".00"){
     #   $suma_factura = $suma_factura -replace ".{3}$"
      #  Write-Output("a intrat aici ma")
    #} 
    write-Output($suma_factura + '    1111111111111111111111111111111')
    $suma_factura = [double]$suma_factura
    Write-Output("suma factuar "+ $suma_factura, $suma_factura.GetType())
    $nr_factura = $data.numar_factura
    $data_factura = $data.data
    $nume_factura = $data.nume_factura
    Write-Output("cont din factura: "+$cont_factura," cui din factura: "+$cui_factura, " suma din factura: "+$suma_factura)
    $data_factura = $data_factura.ToString("MM/dd/yyyy")
    $data_factura =  [datetime]::parseexact($data_factura, 'dd/MM/yyyy', $null)

    
    if($nr_factura -eq "null" -or $nr_factura -eq $null -or $nr_factura -eq '0' -or $nr_factura -eq '00' -or $nr_factura -eq '000' -or $nr_factura -eq '0000' ){
        $reason = $reason + "Numar factura inexistent | "
        $validate = $false
    }
    $cui_client = $cui_client.Replace(" ","")
    $grup = $dict[$cui_client]
    #$reason_cui = ''
    $cui_client_gresit = $false
    if($grup -eq $null -or $grup -eq "null"){
        $reason = $reason + "CUI CLIENT gresit | "
        $cui_client_gresit = $true
        $validate = $false
    }


[string]$searchSQL = "SELECT id_firma, cod_fiscal, denumire FROM firme_master WHERE cod_fiscal = '$cui_factura'";
	
$cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
    $cmd.CommandTimeout=$QueryTimeout
    $ds_firma=New-Object system.Data.DataSet
    $da_firma=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
    [void]$da_firma.fill($ds_firma)
    $ds_firma.Tables[0]

    $id_firma = $ds_firma.Tables[0].id_firma
    $cod_fiscal = $ds_firma.Tables[0].cod_fiscal
    $denumire_firma = $ds_firma.Tables[0].denumire


    if($id_firma -eq $null){
        $cui_factura = $cui_factura.Replace("RO","")
        $cui_factura = $cui_factura.Replace("ro","")
        $cui_factura = $cui_factura.Replace("R O","")
        [string]$searchSQL = "SELECT id_firma, cod_fiscal,denumire FROM firme_master WHERE cod_fiscal = '$cui_factura'";
	
        $cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
        $cmd.CommandTimeout=$QueryTimeout
        $ds_firma=New-Object system.Data.DataSet
        $da_firma=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
        [void]$da_firma.fill($ds_firma)
        $ds_firma.Tables[0]
    
        $id_firma = $ds_firma.Tables[0].id_firma
        $cod_fiscal = $ds_firma.Tables[0].cod_fiscal
        $denumire_firma = $ds_firma.Tables[0].denumire
    }
    if($id_firma -eq $null -or $id_firma -eq 'null' ){
        $cui_factura = $cui_factura.Insert(0,"RO")
        [string]$searchSQL = "SELECT id_firma, cod_fiscal,denumire FROM firme_master WHERE cod_fiscal = '$cui_factura'";
	
        $cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
        $cmd.CommandTimeout=$QueryTimeout
        $ds_firma=New-Object system.Data.DataSet
        $da_firma=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
        [void]$da_firma.fill($ds_firma)
        $ds_firma.Tables[0]
    
        $id_firma = $ds_firma.Tables[0].id_firma
        $cod_fiscal = $ds_firma.Tables[0].cod_fiscal
        $denumire_firma = $ds_firma.Tables[0].denumire
    }
    

    $cui_furnizor_gresit = $false
    if($id_firma -eq $null -or $id_firma -eq 'null' ){
        $reason_cui = $reason_cui + "CUI FURNIZOR gresit | "
        $cui_furnizor_gresit = $true
    }

    class Medic {
        [string]$nume
        [string]$id
        [string]$cod
        [string]$intern_extern
        [bool]$activ
        [float]$suma_actuala
        [float]$suma_luna_trecuta
        [float]$suma_finala
        [string]$cautare
        [bool]$inregistrat
        [string]$IBAN
        [string]$reprezentant
        [bool]$verif_cmr_malpraxis

    }
    $medici_din_clasa=@()
    $medici_din_clasa.Clear()
[string]$searchSQL = "SELECT activ, ent_juridica, medic, denumire, id_forma_contr, cod, reprezentant_hr  FROM medici_master WHERE id_firma_master = '$id_firma'";


	
    $cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
    $cmd.CommandTimeout=$QueryTimeout
    $ds_medic=New-Object system.Data.DataSet
    $da_medic=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
    [void]$da_medic.fill($ds_medic)
    $ds_medic.Tables[0]
    Write-Output("------------------------------------------------------------------------------------------"+$ds_medic.Tables[0].activ)
    $IBAN = @()
    $IBAN = $ds_medic.Tables[0].ent_juridica[0]
    if($IBAN.Length -eq 1){
        $IBAN = $ds_medic.Tables[0].ent_juridica
    }
    $IBAN = $IBAN -replace '\s',''
    $IBAN = $IBAN -replace ' ',''
    

    $medic_extern = $false
    # VERIFICA DACA E MEDIC EXTERN, ELSE: MEDIC INTERN
    if(!$ds_medic.Tables[0].medic){   
        [string]$searchSQL = "SELECT cont, id_medicext, nume, prenume, cod_parafa, reprezentant_hr  FROM medici_externi WHERE id_firma_master = '$id_firma'";
        $cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
        $cmd.CommandTimeout=$QueryTimeout
        $ds_extern=New-Object system.Data.DataSet
        $da_extern=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
        [void]$da_extern.fill($ds_extern)
        $ds_extern.Tables[0]

        $id_medic = $ds_extern.Tables[0].id_medicext
        
        $IBAN = $ds_extern.Tables[0].cont
        $IBAN = $IBAN -replace '\s',''
        $IBAN = $IBAN -replace ' ',''
        if($id_medic.Length -gt 1){
            for($i=0;$i -lt $id_medic.Length;$i++){

                $denumire_medic = $ds_extern.Tables[0].nume[$i] +" "+ $ds_extern.Tables[0].prenume[$i] 

                $cod = $ds_extern.Tables[0].cod_parafa

                $reprezentant_hr = $ds_extern.Tables[0].reprezentant_hr[$i]
                $id_forma_contr = "Extern"
                $medic_extern = $true
                
                $medic = [Medic]::new()
                $medic.id = $id_medic[$i]
                $medic.nume = $denumire_medic
                $medic.cod = $cod
                $medic.reprezentant = $reprezentant_hr
                $medic.intern_extern = $id_forma_contr
                $medic.activ = $true
                $medic.IBAN = $IBAN

                $medici_din_clasa += $medic
                Write-Output("1111111111 EXTERN SI SA VEDEM NUMELE: "+$denumire_medic)
            }
        }else{

            $denumire_medic = $ds_extern.Tables[0].nume +" "+ $ds_extern.Tables[0].prenume
            $cod = $ds_extern.Tables[0].cod_parafa
            Write-Output("222222222222 EXTERN SI SA VEDEM NUMELE: "+$denumire_medic)
            $reprezentant_hr = $ds_extern.Tables[0].reprezentant_hr[0]
            $id_forma_contr = "Extern"
            $medic_extern = $true
        
            $medic = [Medic]::new()
            $medic.id = $id_medic
            $medic.nume = $denumire_medic
            $medic.cod = $cod
            $medic.reprezentant = $reprezentant_hr
            $medic.intern_extern = $id_forma_contr
            $medic.activ = $true
            $medic.IBAN = $IBAN

            $medici_din_clasa += $medic
        }

        if(!$id_medic){
            $reason = $reason + 'Firma nu are medic atribuit | '
        }
    }else{

        $id_forma_contr = "Intern"


        $all_medics = $ds_medic.Tables[0].medic

        Write-Output("alll medics "+$all_medics)

        $id_medic = @()
        for($m=0;$m -lt $all_medics.length; $m++){
            
            $id_medic +=$all_medics[$m]

            $verif = [string]$ds_medic.Tables[0].activ[$m]
            $denumire_medic = $ds_medic.Tables[0].denumire[$m]
            if($all_medics.length -eq 1){
                $denumire_medic = $ds_medic.Tables[0].denumire
            }

            $cod = $ds_medic.Tables[0].cod[$m]
            if($all_medics.length -eq 1){
                $cod = $ds_medic.Tables[0].cod
            }

            $reprezentant_hr = $ds_medic.Tables[0].reprezentant_hr[$m]

            $medic = [Medic]::new()
            $medic.id = $all_medics[$m]
            $medic.nume = $denumire_medic
            $medic.cod = $cod
            $medic.reprezentant = $reprezentant_hr
            $medic.intern_extern = $id_forma_contr
            $medic.IBAN = $IBAN

            if($verif -eq '1'){
                $medic.activ = $true
            }else{
                $medic.activ = $false
            }

            $medici_din_clasa += $medic
            
            [string]$searchSQL = "SELECT cont, id_medicext, nume, prenume, cod_parafa, reprezentant_hr  FROM medici_externi WHERE id_firma_master = '$id_firma'";
            $cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
            $cmd.CommandTimeout=$QueryTimeout
            $ds_extern=New-Object system.Data.DataSet
            $da_extern=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
            [void]$da_extern.fill($ds_extern)
            $ds_extern.Tables[0]

            $id_medic = $ds_extern.Tables[0].id_medicext
            
            if($id_medic){
            
                if($id_medic.Length -gt 1){
                    for($i=0;$i -lt $id_medic.Length;$i++){
                        $IBAN = $ds_extern.Tables[0].cont[$i]
                        $IBAN = $IBAN -replace '\s',''
                        $IBAN = $IBAN -replace ' ',''

                        $denumire_medic = $ds_extern.Tables[0].nume[$i] +" "+ $ds_extern.Tables[0].prenume[$i]
                        $cod = $ds_extern.Tables[0].cod_parafa[$i]
                        $reprezentant_hr = $ds_extern.Tables[0].reprezentant_hr[$i]
                        $id_forma_contr = "Extern"
                        $medic_extern = $true
                        $IBAN = $ds_extern.Tables[0].cont[$i]
                
                        $medic = [Medic]::new()
                        $medic.id = $id_medic[$i] 
                        $medic.nume = $denumire_medic
                        $medic.cod = $cod
                        $medic.reprezentant = $reprezentant_hr
                        $medic.intern_extern = $id_forma_contr
                        $medic.activ = $true
                        $medic.IBAN = $IBAN

                        $medici_din_clasa += $medic
                    }
                }else{

                    $denumire_medic = $ds_extern.Tables[0].nume +" "+ $ds_extern.Tables[0].prenume
                    $cod = $ds_extern.Tables[0].cod_parafa
                    $reprezentant_hr = $ds_extern.Tables[0].reprezentant_hr[0]
                    $id_forma_contr = "Extern"
                    $medic_extern = $true
                    $IBAN = $ds_extern.Tables[0].cont
        
                    $medic = [Medic]::new()
                    $medic.id = $id_medic
                    $medic.nume = $denumire_medic
                    $medic.cod = $cod
                    $medic.reprezentant = $reprezentant_hr
                    $medic.intern_extern = $id_forma_contr
                    $medic.activ = $true
                    $medic.IBAN = $IBAN

                    $medici_din_clasa += $medic
                }
            }
        }
    }

        
   # for($i=0; $i -lt $medici_din_clasa.Length; $i++){
   #     Write-Output("AICI PRINTEZ OBIECTELE: "+$medici_din_clasa[$i].nume)
   # }

    #aici atribui sumele de luna asta si luna trecuta fiecarui medic in parte
    Write-Output("AICI PRINTEZ OBIECTELE: "+$medici_din_clasa.Length)
    $numardetest = 0
    for($i=0; $i -lt $medici_din_clasa.Length; $i++){
        Write-Output("AICI PRINTEZ OBIECTELE: "+$medici_din_clasa[$i].nume)
         Write-Output("activ: "+$medici_din_clasa[$i].activ)
         $numardetest =  $numardetest + 1
        if($medici_din_clasa[$i].activ -eq $true){
            if($medici_din_clasa[$i].intern_extern -eq 'Intern'){
                [string]$searchSQL = "SELECT TOP 2 * FROM pm_facturi WHERE medic = 'I_"+$medici_din_clasa[$i].id+"' AND grup = '"+$dict[$cui_client]+"' ORDER BY id_pm_facturi DESC ";
                $cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
                $cmd.CommandTimeout=$QueryTimeout
                $ds_intern=New-Object system.Data.DataSet
                $da_intern=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
                [void]$da_intern.fill($ds_intern)
                $ds_intern.Tables[0]

            }else{
                [string]$searchSQL = "SELECT TOP 2 * FROM pm_facturi WHERE medic = 'E_"+$medici_din_clasa[$i].id+"' AND grup = '"+$dict[$cui_client]+"' ORDER BY id_pm_facturi DESC ";
                   $cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
                $cmd.CommandTimeout=$QueryTimeout
                $ds_intern=New-Object system.Data.DataSet
                $da_intern=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
                [void]$da_intern.fill($ds_intern)
                $ds_intern.Tables[0]
            }
            
            for($top_2 = 0; $top_2 -lt 2; $top_2++){
                $an_factura = $ds_intern.Tables[0].an[$top_2]
                
                $luna_factura = $ds_intern.Tables[0].luna[$top_2]

                $an_factura = [int]$an_factura
                $luna_factura = [int]$luna_factura
                $today =  [datetime]::parseexact($today, 'dd/MM/yyyy', $null)
                Write-Output("sume: "+$ds_intern.Tables[0].valoare[$top_2])
                Write-Output("---")
                if($an_factura -eq $today.Year -and $luna_factura -eq ($today.AddMonths(-1).Month) -or $an_factura -eq ($today.Year-1) -and $luna_factura -eq ($today.AddMonths(-1).Month)){
                    if($top_2 -eq 0){
                        $medici_din_clasa[$i].suma_actuala = $ds_intern.Tables[0].valoare[$top_2]
                        $an_sikulix = $an_factura
                        $luna_sikulix = $luna_factura
                    }else{
                        $medici_din_clasa[$i].suma_luna_trecuta = $ds_intern.Tables[0].valoare[$top_2]
                        $an_sikulix = $an_factura
                        $luna_sikulix = $luna_factura
                    }
            }
        }
    }
    }
    $validate = $true

    # aici incep verificarile

    # aici verific SUMA; care suma e cea corecta, a acui si de pe ce luna.
    $suma_verificare = "ERROR"
    [float]$suma_colectiva = 0
    #for($i=0; $i -lt $medici_din_clasa.Length; $i++){
        Write-Output($medici_din_clasa[$i].suma_actuala)
    #}
    Write-Output($suma_factura)
    
    for($i=0; $i -lt $medici_din_clasa.Length; $i++){
        if($medici_din_clasa[$i].activ -eq $true){
            
            $suma_colectiva = $suma_colectiva + $medici_din_clasa[$i].suma_actuala
            if([Math]::Abs($suma_factura - $medici_din_clasa[$i].suma_actuala) -le 0.99){
                $medici_din_clasa[$i].suma_finala = $medici_din_clasa[$i].suma_actuala
                $medici_din_clasa[$i].verif_cmr_malpraxis = $true
                $suma_verificare = "PASS"
            }elseif([Math]::Abs($suma_factura - $medici_din_clasa[$i].suma_luna_trecuta) -le 0.99){
                $medici_din_clasa[$i].suma_finala = $suma_factura
                $medici_din_clasa[$i].verif_cmr_malpraxis = $true
                $suma_verificare = "PASS"
            }
        }
    }
    Write-Output("deasupra suma colectiva")
    Write-Output($suma_colectiva)
    Write-Output("sumaverif"+$suma_verificare)
    $verificare_toti = $false
    if($suma_verificare -eq "ERROR"){
        if([Math]::Abs($suma_factura - $suma_colectiva) -le 0.99){
            $medici_din_clasa[0].suma_finala = $suma_factura
            for($i=0;$i -lt $medici_din_clasa.Length; $i ++){
                $medici_din_clasa[$i].verif_cmr_malpraxis = $true
            }
            $verificare_toti = $true
            $suma_verificare = "PASS"
        }else{
            $validate = $false
            $reason = "Suma nu coincide - Factura: "+$suma_factura + " DB: "+$suma_colectiva+ " | "
        }
    }

    #doar printez ceva

    #for($i=0;$i -lt $medici_din_clasa.Length; $i ++){
    #        Write-Output("medicul: "+$medici_din_clasa[$i].nume+" suma lui: "+$medici_din_clasa[$i].suma_finala+ " ibanul lui: "+$medici_din_clasa[$i].IBAN)
    #}


    #aici verific IBANUL
    Write-Output("IBANUL DE PE FACTURA: "+$cont_factura)
    
    for($i=0; $i -lt $medici_din_clasa.Length; $i++){
    Write-Output("IBANUL DIN DB: "+$medici_din_clasa[$i].IBAN)
        $medici_din_clasa[$i].IBAN = $medici_din_clasa[$i].IBAN -replace " ",""
        if($verificare_toti -eq $true){
            
            if([string]$medici_din_clasa[$i].IBAN -eq [string]$cont_factura){
                $IBAN_verificare = "PASS"
                Write-Output("if if:")
            }else{
                Write-Output("if else:")
                $IBAN_verificare = "ERROR"
                $validate = $false
                $reason = $reason + "IBAN-ul nu coincide (Factura-DB) | "
            }
        }elseif($medici_din_clasa[$i].suma_finala -ne 0){
            if([string]$medici_din_clasa[$i].IBAN -eq [string]$cont_factura){
                $IBAN_verificare = "PASS"
                Write-Output("else if if:")
            }else{
                Write-Output("else if else:")
                $IBAN_verificare = "ERROR"
                $validate = $false
                $reason = $reason + "IBAN-ul nu coincide (Factura-DB) | "
            }
        }
        Write-Output("IBAN verificare: "+$IBAN_verificare)
        Write-Output("reason: "+$reason)
    }


            
    # aici verificare data factura

    $verificare_data_factura = ""
  
    $today = Get-Date -Format "dd/MM/yyyy"
    $today = [datetime]::parseexact($today, 'dd/MM/yyyy', $null)
    $data_de_verificat =  [datetime]::parseexact($data_factura, 'dd/MM/yyyy', $null)
    $today_verificare = [datetime]::parseexact($today, 'dd/MM/yyyy', $null)

    $data_verificat = Get-Date $data_factura
    $data_verificat = [datetime]::parseexact($data_factura, 'dd/MM/yyyy', $null)
    $lastDay = [DateTime]::DaysInMonth($data_verificat.Year, ($data_verificat.Month-1))
    $lastMonth = $today.AddMonths(-1).Month
    $count_days = $lastDay - $data_verificat.Day
    
    if($data_verificat.Month -eq $today.Month){
        $verificare_data_factura = "PASS"
    }else{
        if($data_verificat.Month -eq $lastMonth -and $data_verificat.Day -ge ($lastDay - 6)){
            $verificare_data_factura = "PASS"
        }else{
            $verificare_data_factura = "ERROR"
            $validate = $false
            $reason = $reason + "Data incorecta | "
        }
    }

    # aici verificare malpraxis cmr

    $data_emitere_malpraxis = "-"
    $data_emitere_cmr = "-"
    
    for($i=0; $i -lt $medici_din_clasa.Length; $i++){
        
        if($medici_din_clasa[$i].verif_cmr_malpraxis -eq $true -and $medici_din_clasa[$i].intern_extern -eq "Intern"){
            [string]$searchSQL = "SELECT emitent, data_emitere, data_expirare  FROM medici_master_ext WHERE medic_master = "+$medici_din_clasa[$i].id+"ORDER BY data_expirare DESC";
            $cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
            $cmd.CommandTimeout=$QueryTimeout
            $ds_ext=New-Object system.Data.DataSet
            $da_ext=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
            [void]$da_ext.fill($ds_ext)
            $ds_ext.Tables[0]

            $date_expirare = @()
            $emitent = @()
            for($p=0; $p -lt $ds_ext.Tables[0].data_expirare.length; $p++){
                
                $date_expirare +=$ds_ext.Tables[0].data_expirare[$p]
                $emitent += $ds_ext.Tables[0].emitent[$p]

            }

            if($judete -contains $emitent[0]){
                $data_expirare_cmr = $date_expirare[0]
                $data_expirare_malpraxis = $date_expirare[1]
            }elseif($judete -contains $emitent[1] ){ #-or $judete -contains $emitent[0]-or $judete -contains $emitent[3]
                $data_expirare_cmr = $date_expirare[1]
                $data_expirare_malpraxis = $date_expirare[0]
            }else{
                $data_expirare_malpraxis = $date_expirare[0]
                $data_expirare_cmr = $date_expirare[1]
                $data_expirare_3 = $date_expirare[2]
            }
            Write-Output($data_expirare_cmr)
            Write-Output("================================================================================================================================================================")
            if( $data_expirare_malpraxis -eq $null -or $data_expirare_cmr -eq $null){
                $reason = $reason + "Data cmr/malpraxis inexsitenta in DB/n pentru medicul cu id: "+$medici_din_clasa[$i].id+" "
            }




            #Verificare cmr SI malpraxis
            # ATENTIE si pentru restul medicilor
            $today    = Get-Date -format "MM/dd/yyyy HH:mm:ss"
            $today = [datetime]::parseexact($today, 'MM/dd/yyyy HH:mm:ss', $null)
            $malpraxis = ""
            $cmr = ""

            $data_verificat = Get-Date $data_factura
            Write-Output("DATA DE VERIFICAT: "+$data_verificat)
            $a_intrat = $false
            if($today.Month -eq $data_verificat.Month + 1){
                #$data_verificat = $data_verificat.AddMonths(-1)
                $lastDay = [DateTime]::DaysInMonth($data_verificat.Year, $data_verificat.Month)
                $count_days = $lastDay - $data_verificat.Day
                $data_verificat = $data_verificat.AddDays($count_days)
                $a_intrat = $true
            }

            if($a_intrat -eq $false){
                $data_verificat = $data_verificat.AddDays(-$data_factura.Day)
            }
            
            #$lastDay = [DateTime]::DaysInMonth($data_verificat.Year, $data_verificat.Month)

           # $count_days = $lastDay - $data_verificat.Day
            #$data_verificat = $data_verificat.AddDays($count_days)
            
            
            Write-Output("DATA DE VERIFICAT: "+$data_verificat)
            Write-Output("DATA CMR: "+$data_expirare_cmr)
            if($data_verificat -le $data_expirare_malpraxis){
                $malpraxis = "PASS"
            }else{
                $malpraxis = "ERROR"
                $validate = $false
                $reason = $reason + "Malpraxis expirat | id medic: "+$medici_din_clasa[$i].id +" | "

            }
           
            if($data_verificat -le $data_expirare_cmr){
                $cmr = "PASS"
            }else{
                $cmr = "ERROR"
                $validate = $false
                $reason = $reason + "CMR expirat | id medic: "+$medici_din_clasa[$i].id +" | "
            }
            Write-Output("REASON DUPA CMR: "+$reason)
        }

    }

$array_nume_medici = @()
$array_id_medici = @()
$array_reprezentanti = @()
$array_cod = @()
for($i=0; $i -lt $medici_din_clasa.Length; $i++){
        $array_nume_medici += $medici_din_clasa[$i].nume
        $array_id_medici += $medici_din_clasa[$i].id
        $array_reprezentanti += $medici_din_clasa[$i].reprezentant
        $array_cod += $medici_din_clasa[$i].cod
}
 Write-Output("id hr: "+$array_reprezentanti)
$array_nume_reprezentanti = @()
for($j=0; $j -lt $array_reprezentanti.Length; $j++){
        $nume_reprezentant = ""
        [string]$searchSQL ="SELECT * FROM nom_reprezentanti WHERE id = '"+$array_reprezentanti[$j]+"'"
        $cmd=new-object System.Data.Odbc.OdbcCommand($searchSQL,$conn)
        $cmd.CommandTimeout=$QueryTimeout
        $ds_hr=New-Object system.Data.DataSet
        $da_hr=New-Object system.Data.odbc.OdbcDataAdapter($cmd)
        [void]$da_hr.fill($ds_hr)
        $ds_hr.Tables[0]
        Write-Output("nume repre : "+$ds_hr.Tables[0].nume)
        $nume_reprezentant += $ds_hr.Tables[0].nume +' '+ $ds_hr.Tables[0].prenume
        $array_nume_reprezentanti += $nume_reprezentant

    }
    Write-Output($array_nume_reprezentanti)
if(!$array_id_medici[0]){
    $reason = "Firma nu are medic atribuit | "
    Write-Output("in if:")
}

$numar_inactivi = 0
for($i=0; $i -lt $medici_din_clasa.Length; $i++){
    if($medici_din_clasa[$i].activ -eq $false){
        $numar_inactivi = $numar_inactivi+1
    }
}

if($medici_din_clasa.Length -eq $numar_inactivi){
    $validate = $false
    $reason = "Medic inactiv | "
}

for($i=0; $i -lt $medici_din_clasa.Length; $i++){


    

            
    $data | Add-Member -Type NoteProperty -Name 'total_db' -Value $suma_colectiva -Force
    $data | Add-Member -Type NoteProperty -Name 'id_firma' -Value $id_firma -Force
    $data | Add-Member -Type NoteProperty -Name 'denumire_firma' -Value $denumire_firma -Force
       
    $data | Add-Member -Type NoteProperty -Name 'id_medic' -Value $array_id_medici -Force

    $data | Add-Member -Type NoteProperty -Name 'denumire_medic' -Value $array_nume_medici  -Force
    $data | Add-Member -Type NoteProperty -Name 'cod' -Value $array_cod -Force
    $data | Add-Member -Type NoteProperty -Name 'reprezentant_hr' -Value $array_nume_reprezentanti -Force
                
    $data | Add-Member -Type NoteProperty -Name 'grup' -Value $grup -Force

    if($medici_din_clasa[$i].intern_extern -eq "Intern"){
        $data | Add-Member -Type NoteProperty -Name 'data_expirare_malpraxis' -Value $data_expirare_malpraxis.ToString("dd/MM/yyyy") -Force
        $data | Add-Member -Type NoteProperty -Name 'data_expirare_cmr' -Value $data_expirare_cmr.ToString("dd/MM/yyyy") -Force
        $data | Add-Member -Type NoteProperty -Name 'verificare_malpraxis' -Value $malpraxis -Force
        $data | Add-Member -Type NoteProperty -Name 'verificare_cmr' -Value $cmr -Force
    }else{
        $data | Add-Member -Type NoteProperty -Name 'data_expirare_malpraxis' -Value "medic_extern" -Force
        $data | Add-Member -Type NoteProperty -Name 'data_expirare_cmr' -Value "medic_extern".ToString("dd/MM/yyyy") -Force
        $data | Add-Member -Type NoteProperty -Name 'verificare_malpraxis' -Value "medic_extern" -Force
        $data | Add-Member -Type NoteProperty -Name 'verificare_cmr' -Value "medic_extern" -Force
    }
                
    $data | Add-Member -Type NoteProperty -Name 'verificare_suma' -Value $suma_verificare -Force
    $data | Add-Member -Type NoteProperty -Name 'verificare_IBAN' -Value $IBAN_verificare -Force
    $data | Add-Member -Type NoteProperty -Name 'verificare_data_factura' -Value $verificare_data_factura -Force
    $data | Add-Member -Type NoteProperty -Name 'verificare_IBAN' -Value $IBAN_verificare -Force



    if($cui_client_gresit -eq $true -or $cui_furnizor_gresit -eq $true){
        $data | Add-Member -Type NoteProperty -Name 'reason' -Value $reason_cui -Force
    }else{
        $data | Add-Member -Type NoteProperty -Name 'reason' -Value $reason -Force
    }
    Write-Output($reason)
    $data | Add-Member -Type NoteProperty -Name 'data_creere' -Value $today.ToString("MM/dd/yyyy HH:mm:ss") -Force
            
                
    #$name = $name +'_'+ $i.ToString()
    if($validate -eq $true){
        $data| ConvertTo-Json -Depth 10 | Out-File "$validate_invoice\$name" -Encoding Ascii
    }else{
        $data| ConvertTo-Json -Depth 10 | Out-File "$validate_error\$name" -Encoding Ascii
    }
    
    #vad daca sunt unu sau mai multi medici
    $one_or_many = 0
    for($s=0; $s -lt $medici_din_clasa.Length; $s++){
        if($medici_din_clasa[$s].verif_cmr_malpraxis -eq $true){
            $one_or_many = $one_or_many +1
        }
    }

    #variabile pentru sikulix

    $cautare_medic = $medici_din_clasa[$i].nume + " - " + $medici_din_clasa[$i].cod

    if($validate -eq $true){
            
        if($medici_din_clasa[$i].verif_cmr_malpraxis -eq $true){
            $al_catelea = $i
            if($i -eq 0){
                $al_catelea=''
            }
            $director_pentru_sikulix = $dir_plm+'search_'+$name+"_"+$al_catelea+'.txt'
            Clear-Content $director_pentru_sikulix

            
            Write-Output("zi data factura "+$data_factura.Day)
            $data_prelucrata = $data_factura.ToString().replace("/","")
            if($data_factura.Month.ToString().Length -eq 1){
            $luna_scris = '0'+$data_factura.Month.ToString()
            }else{
                $luna_scris = $data_factura.Month.ToString()
            }
            if($data_factura.Day.ToString().Length -eq 1){
                $zi_scris = '0'+$data_factura.Day.ToString()
            }else{
                $zi_scris = $data_factura.Day.ToString()
            }
            $data_prelucrata = $zi_scris + $luna_scris + $data_factura.Year.ToString()
            Write-Output("data prelucrata: "+$data_prelucrata)
                
                
            $cautare_medic | Add-Content $director_pentru_sikulix
            Write-Output("========================================================= multi true "+$cautare_medic)
            if($medici_din_clasa[$i].intern_extern -eq "Extern"){
                $forma_contractuala = "Extern"
            }else{
                $forma_contractuala = "Intern"
            }
            $forma_contractuala | Add-Content $director_pentru_sikulix

            $year = get-date -Format yyyy
            $month = get-date -Format MM

            $an_sikulix | Add-Content $director_pentru_sikulix
            $luna_sikulix | Add-Content $director_pentru_sikulix
            $nr_factura | Add-Content $director_pentru_sikulix
            $data_prelucrata | Add-Content $director_pentru_sikulix
            $medici_din_clasa[$i].suma_finala | Add-Content $director_pentru_sikulix
            $grup | Add-Content $director_pentru_sikulix
            if($one_or_many -eq 1){
                "one" | Add-Content $director_pentru_sikulix
            }else{
                "more" | Add-Content $director_pentru_sikulix
            }
            $nume_factura | Add-Content $director_pentru_sikulix
            $denumire_firma | Add-Content $director_pentru_sikulix
            $array_nume_reprezentanti[$i] | Add-Content $director_pentru_sikulix
            $conn.Close()
            
        }
            
        if($medici_din_clasa[$i].verif_cmr_malpraxis -eq $false){
            $al_catelea = $i
            if($i -eq 0){
                $al_catelea=''
            }
            $director_pentru_sikulix = $dir_plm+'search_'+$name+"_"+$al_catelea+'.txt'
            Clear-Content $director_pentru_sikulix

            
            Write-Output("zi data factura "+$data_factura.Day)
            $data_prelucrata = $data_factura.ToString().replace("/","")
            if($data_factura.Month.ToString().Length -eq 1){
                $luna_scris = '0'+$data_factura.Month.ToString()
            }else{
                $luna_scris = $data_factura.Month.ToString()
            }
            if($data_factura.Day.ToString().Length -eq 1){
                $zi_scris = '0'+$data_factura.Day.ToString()
            }else{
                $zi_scris = $data_factura.Day.ToString()
            }
            $data_prelucrata = $zi_scris + $luna_scris + $data_factura.Year.ToString()
            Write-Output("data prelucrata: "+$data_prelucrata)
                
                
            $cautare_medic | Add-Content $director_pentru_sikulix
            Write-Output("========================================================= multi true "+$cautare_medic)
            if($medici_din_clasa[$i].intern_extern -eq "Extern"){
                $forma_contractuala = "Extern"
            }else{
                $forma_contractuala = "Intern"
            }
            $forma_contractuala | Add-Content $director_pentru_sikulix

            $year = get-date -Format yyyy
            $month = get-date -Format MM

            $year | Add-Content $director_pentru_sikulix
            $month | Add-Content $director_pentru_sikulix
            $nr_factura | Add-Content $director_pentru_sikulix
            $data_prelucrata | Add-Content $director_pentru_sikulix
            "0" | Add-Content $director_pentru_sikulix
            $grup | Add-Content $director_pentru_sikulix
            if($one_or_many -eq 1){
                "one" | Add-Content $director_pentru_sikulix
            }else{
                "more" | Add-Content $director_pentru_sikulix
            }
            $nume_factura | Add-Content $director_pentru_sikulix
            $denumire_firma | Add-Content $director_pentru_sikulix
            $array_nume_reprezentanti[$i] | Add-Content $director_pentru_sikulix
            $conn.Close()
            
        }

    }else{
        # set sikulix variables
        $al_catelea = $i
        if($i -eq 0){
            $al_catelea=''
        }
        $director_pentru_sikulix = $dir_plm_error+'\search_'+$name+"_"+$al_catelea+'.txt'
        

        Clear-Content $director_pentru_sikulix

        Write-Output("zi data factura "+$data_factura.Day)
            $data_prelucrata = $data_factura.ToString().replace("/","")
        
        if($data_factura.Month.ToString().Length -eq 1){
            $luna_scris = '0'+$data_factura.Month.ToString()
        }else{
            $luna_scris = $data_factura.Month.ToString()
        }
        if($data_factura.Day.ToString().Length -eq 1){
            $zi_scris = '0'+$data_factura.Day.ToString()
        }else{
            $zi_scris = $data_factura.Day.ToString()
        }
        $data_prelucrata = $zi_scris + $luna_scris + $data_factura.Year.ToString()
        Write-Output("data prelucrata: "+$data_prelucrata)

        $cautare_medic | Add-Content $director_pentru_sikulix
        Write-Output("========================================================= multi true "+$cautare_medic)
        if($medici_din_clasa[$i].intern_extern -eq "Extern"){
            $forma_contractuala = "Extern"
        }else{
            $forma_contractuala = "Intern"
        }
        $forma_contractuala | Add-Content $director_pentru_sikulix

        $year = get-date -Format yyyy
        $month = get-date -Format MM

        $year| Add-Content $director_pentru_sikulix
        $month | Add-Content $director_pentru_sikulix
        $nr_factura | Add-Content $director_pentru_sikulix
        $data_prelucrata | Add-Content $director_pentru_sikulix
        $medici_din_clasa[$i].suma_finala | Add-Content $director_pentru_sikulix
        $grup | Add-Content $director_pentru_sikulix
        if($one_or_many -eq 1){
            "one" | Add-Content $director_pentru_sikulix
        }else{
            "more" | Add-Content $director_pentru_sikulix
        }
        $nume_factura | Add-Content $director_pentru_sikulix
        $denumire_firma | Add-Content $director_pentru_sikulix
        $array_nume_reprezentanti[$i] | Add-Content $director_pentru_sikulix
        $conn.Close()
            
        }
    }
    Move-Item -Path "$outfile" -Destination "$procesate\$f"
}

Write-Output($numardetest)
$conn.Close()