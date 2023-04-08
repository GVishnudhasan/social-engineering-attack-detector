import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ReportingFormComponent } from './reporting-form/reporting-form.component';

const routes: Routes = [
  {
  path: 'reporting-form', 
  component: ReportingFormComponent,
  },
  {
    path: '',
    redirectTo: 'reporting-form',
    pathMatch: 'full',
  },
  {
    path: '**',
    redirectTo: 'reporting-form',
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
