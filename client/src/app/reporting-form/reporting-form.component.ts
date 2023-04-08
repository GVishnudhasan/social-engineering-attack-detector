import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
// import { MatSnackBar } from '@angular/material/snack-bar';

const BACKEND_URL = 'http://localhost:8080/';

interface SuspiciousIdsResponse {
  suspicious_ids: string[];
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
};

@Component({
  selector: 'app-reporting-form',
  templateUrl: './reporting-form.component.html',
  styleUrls: ['./reporting-form.component.css'],
})
export class ReportingFormComponent implements OnInit {
  reportingForm: FormGroup | any;
  suspiciousIds: Array<String> = [];

  constructor(private fb: FormBuilder, private http: HttpClient) {}

  ngOnInit(): void {
    this.reportingForm = this.fb.group({
      socialMediaPlatform: ['', Validators.required],
      id: ['', Validators.required],
    });
  }

  onSubmit() {
    console.log(this.reportingForm.value);
    const data = {
      socialMediaPlatform: this.reportingForm.value.socialMediaPlatform,
      id: this.reportingForm.value.id,
    };
    this.http.post(BACKEND_URL + 'report', data, httpOptions).subscribe(
      (response: any) => {
        console.log(response);

        this.suspiciousIds = response.suspicious_ids;
        console.log(this.suspiciousIds);
      },
      (error) => {
        console.log(error);
      }
    );
  }
}
