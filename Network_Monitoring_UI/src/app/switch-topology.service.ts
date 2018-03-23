import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions } from '@angular/http';
import { SwitchTopology } from './switch-topology';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class SwitchTopologyService {
	private domain = "http://localhost:8080/";
	private authUrl = this.domain + 'network_monitoring/login';
	//private authUrl = 'http://demo0509553.mockable.io/authenticate';
	//private switchTopologiesUrl = 'assets/data/switch-topologies.json';
	private switchTopologiesUrl = this.domain + "switches";
	//private flowsUrl = 'assets/data/flows.json';
	private flowsUrl = this.domain + "flows";
	private topologyUrl = this.domain + 'network_monitoring/topology';
	//private flowMetricsUrl = 'assets/data/flow-metrics.json';
	private flowMetricsUrl = this.domain + 'flow_metrics';
	//private flowDetailsUrl = 'assets/data/flow-details.json';
	private flowDetailsUrl = this.domain + "flow_details";

	constructor(private http: Http) { }

	authenticate(userData): Promise<any> {
		const headers = new Headers();
        headers.append('Content-Type', 'application/json');
		const options = new RequestOptions({headers: headers});
		
		return this.http.post(this.authUrl, userData, options)
           .toPromise()
           .then(response => response.json().status as any[])
           .catch(this.handleError);
	}

	getSwitchTopologies(): Promise<SwitchTopology[]> {
		return this.http.get(this.switchTopologiesUrl)
           .toPromise()
           .then(response => response.json().Active_Switches as SwitchTopology[])
           .catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		return Promise.reject(error.message || error);
	}
	
	getTopology(): Promise<any> {
		return this.http.get(this.topologyUrl)
           .toPromise()
           .then(response => response.json().Network_Topology as any)
           .catch(this.handleError);
	}

	getFlowMetrics(switchID: string): Promise<any> {
		return this.http.get(this.flowMetricsUrl +"/node/"+ switchID)
           .toPromise()
           .then(response => response.json().Flow_Metrics as any)
           .catch(this.handleError);
	}

	getFlows(switchID: string): Promise<any> {
		//return this.http.post(this.flowsUrl, {"switchID": switchID})
		return this.http.get(this.flowsUrl +"/node/"+ switchID)
           .toPromise()
           .then(response => response.json().Active_Flows as any[])
           .catch(this.handleError);
	}

	getFlowDetails(switchID: string, flow: string): Promise<SwitchTopology> {
		//return this.http.post(this.flowDetailsUrl, {"switchID": switchID, "flow": flow})
		return this.http.get(this.flowDetailsUrl +"/node/"+ switchID + "/flow/"+ flow)
           .toPromise()
           .then(response => response.json().Flow_Details as any)
           .catch(this.handleError);
	}
}
