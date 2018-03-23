import { Component, OnInit } from '@angular/core';
import { SwitchTopology } from './switch-topology';
import { Switch } from './switch';
import { SwitchTopologyService } from './switch-topology.service';

@Component({
  selector: 'app-switch-topologies',
  templateUrl: './switch-topologies.component.html',
  styleUrls: ['./switch-topologies.component.css']
})
export class SwitchTopologiesComponent implements OnInit {

  switchTopologies: SwitchTopology[];
  selectedSwitch: string;
  selectedFlow: string;
  flows: any[] = [];
  controller = {"uname": "", "passwd": "", "ip": ""};
  userData = {};
  topology = "";
  flowMetrics = {};
  flowDetails = {};

  //@ViewChild('treeNo1')
  //private treeNo1: NgTree;

  public treeData: any[] = [];

  public treeConfig : any = {
    onFold: (node: any): boolean => {
      //console.log(this.treeNo1.searchNodes(null, { name: "00:00:00:00:00:00:00:01" }));
      //this.getFlows(node.name);
      this.selectedSwitch = node.name;
      this.switchTopologyService.getFlows(this.selectedSwitch)
		.then(flows => {
		  node.children = [];
		  this.flows = flows;
		  this.flows.forEach(element => {
			node.children.push({"name": element, "parent": this.selectedSwitch});
		  });
		  
		  //this.getFlowMetrics(this.selectedSwitch);
		});
      return true;
    },

    onClick: (node: any): void => {
	  if(node.parent) {
		  this.selectedFlow = node.name;
		  this.selectedSwitch = node.parent;
		  this.getFlowDetails(this.selectedSwitch, this.selectedFlow);
	  } else {
		  this.selectedSwitch = node.name;
	  }
    }
  }

  constructor(private switchTopologyService: SwitchTopologyService) { }

  ngOnInit(): void {
    //this.getSwitchTopologies();
  }

  authenticateUser(): void {
    this.userData = {
      "username": this.controller.uname,
      "password": this.controller.passwd,
      "ip": this.controller.ip
    };

    this.switchTopologyService.authenticate(this.userData)
    .then(authResponse => {
      if(authResponse == 'ok') {
        this.getSwitchTopologies();
        this.getFlowMetrics();
      }
    });
  }

  getSwitchTopologies(): void {
    this.treeData = [];
    this.switchTopologyService.getSwitchTopologies()
    .then(switchTopologies => {
      this.switchTopologies = switchTopologies;
      this.switchTopologies.forEach(element => {
        this.treeData.push({
          "name": element.name,
          "isOpen":false,
          "iconSelector":"computer",
          "nameSelector":"warning",
          "children": []
        });
      });
	  
	  this.getTopology();
    });
  }

  getTopology(): void {
    this.switchTopologyService.getTopology()
    .then(topology => {
      this.topology = topology;
    });
  }
  
  getFlowMetrics(): void {
    this.switchTopologyService.getFlowMetrics(this.selectedSwitch)
    .then(flowMetrics => {
      this.flowMetrics = flowMetrics;
    });
  }

  /*getFlows(switchID: string): void {
    this.selectedSwitch = switchID;
    this.switchTopologyService.getFlows(this.selectedSwitch)
              .then(flows => this.flows = flows);
  }*/

  getFlowDetails(switchID: string, flow: string): void {
    this.switchTopologyService.getFlowDetails(switchID, flow)
              .then(flowDetails => this.flowDetails = flowDetails);
  }
}
