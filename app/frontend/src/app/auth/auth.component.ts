import { Component, OnInit, ViewChild, ViewContainerRef, NgModule } from '@angular/core';
import { HomeComponent } from '../home/home.component';
import { LoadingService } from '../loading.service';
import { FormsModule } from '@angular/forms';
import { DataSendService } from '../api-client.service';
import { DynamicComponentService } from '../dynamic-component.service';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [
    HomeComponent,
    FormsModule,
  ],
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.css'
})
export class AuthComponent implements OnInit {

  @ViewChild('dynamicComponentContainer', { read: ViewContainerRef, static: true })
  dynamicComponentContainer!: ViewContainerRef;

  constructor(
    private loadingService: LoadingService,
    private dataSendService: DataSendService,
    private dynamicComponentService: DynamicComponentService,  ){}

    loadComponent(component: any) {
      this.dynamicComponentService.loadComponent(this.dynamicComponentContainer, component);
    }

  pass = '';

  auth_hidden_class = false

  send_pass(){
    this.dataSendService.sendData(this.pass);
    this.auth_hidden_class = true;
    this.loadComponent(HomeComponent);
  }

  ngOnInit(): void {
    this.loadingService.simulateLoading();
  }

}
