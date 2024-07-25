// orders.component.ts
import { ScrollProgressBarComponent } from '../scroll-progress-bar/scroll-progress-bar.component';
import { LoadingService } from '../loading.service';
import { Component, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import { DynamicComponentService } from '../dynamic-component.service';
import { CommonModule } from '@angular/common';
import { ReportComponent } from '../report/report.component';
import { ProductsComponent } from '../products/products.component';
import { TargetComponent } from '../target/target.component';

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [ScrollProgressBarComponent,
    CommonModule,
    ProductsComponent,
    TargetComponent
  ],
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {

  orders_show = false;

  @ViewChild('dynamicComponentContainer', { read: ViewContainerRef, static: true })
  dynamicComponentContainer!: ViewContainerRef;

  orders = [
    { id: '12345', totalPayment: 150.00, date: new Date('2024-07-15'), details: 'Order details for 12345' },
    { id: '12346', totalPayment: 250.00, date: new Date('2024-07-16'), details: 'Order details for 12346' },
    // Add more orders as needed
  ];

  selectedOrder: any = null;

  constructor(
    private loadingService: LoadingService,
    private LoadComponent: DynamicComponentService
  ){}

  componentLoad(component: any){
    this.LoadComponent.loadComponent(this.dynamicComponentContainer, component);
  }

  logBtn(){
    this.componentLoad(ReportComponent);
this.orders_show = true;
  };
  productsBtn(){
    this.componentLoad(ProductsComponent);
this.orders_show = true;
  };
  targetBtn(){
    this.componentLoad(TargetComponent);
this.orders_show = true;
  };

  ngOnInit(): void {
    this.loadingService.simulateLoading();
  }
}
