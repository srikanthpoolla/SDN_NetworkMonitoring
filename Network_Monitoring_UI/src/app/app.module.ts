import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { NgTree } from "ng.tree";

import { AppComponent } from './app.component';
import { SwitchTopologiesComponent } from './switch-topologies.component';

import { SwitchTopologyService } from './switch-topology.service';

@NgModule({
  declarations: [
    AppComponent,
    SwitchTopologiesComponent,
    NgTree
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [SwitchTopologyService],
  bootstrap: [AppComponent]
})
export class AppModule { }
