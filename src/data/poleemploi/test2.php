<?php
/**
 * Created by PhpStorm.
 * User: sebastien
 * Date: 3/25/17
 * Time: 8:37 PM
 */

$client_id = "PAR_jobtrends_b63b357cc6230d496bf4e4263b8d0b7b1e29178163aa9e44db0a496cd76f61a7";
$client_secret = "e9c3ae0584e0f59734efcf25886337fec6409c54273c2371a637a74980fb4e76";
$token_url = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token';

$apiURLBase = 'https://api.emploi-store.fr/partenaire/infotravail/v1/';

$start = null;
$offset = 11500;
$next = "datastore_search?resource_id=421692f5-f342-4223-9c51-72a27dcaf51e&offset=".$offset;

while (!$start || $next != $start)
{

    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $token_url."?realm=partenaire");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS,
        http_build_query(array("grant_type" => "client_credentials",
            "client_id" => $client_id,
            "client_secret" => $client_secret,
            "scope" => "api_infotravailv1 application_".$client_id)));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $server_output = curl_exec ($ch);
    $server_output = json_decode($server_output, true);

    $token = $server_output["access_token"];

    curl_close($ch);

    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $apiURLBase . $next."&");
    curl_setopt($ch, CURLOPT_POST, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER,
        array("Authorization: Bearer " . $token));

    $server_output = curl_exec($ch);
    echo $server_output;

    curl_close($ch);

    var_dump($server_output);

    $server_output = json_decode($server_output, true);

    var_dump($server_output);

    if (key_exists("resource_id", $server_output["result"]))
        echo ("found!");


    $myfile = fopen("list_offres/".$server_output["result"]["resource_id"].$offset.".json", "w");
    fwrite($myfile, json_encode($server_output["result"]));
    fclose($myfile);

    $offset += intval(sizeof($server_output["result"]["records"]));

    $next = "datastore_search?resource_id=421692f5-f342-4223-9c51-72a27dcaf51e&offset=".$offset;
    echo $next;
    sleep(11);
}