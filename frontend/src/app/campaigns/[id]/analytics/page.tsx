"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardContent, Button } from "@/lib/ui";
import { AlertTriangle, TrendingUp, DollarSign, MousePointerClick, CheckCircle } from "lucide-react";
import { CampaignAnalyticsReport } from "@/lib/types";

export default function CampaignAnalyticsPage() {
  const params = useParams();
  const campaignId = params.id as string;

  const [report, setReport] = useState<CampaignAnalyticsReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    loadAnalytics();
  }, [campaignId]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const data = await api.getCampaignAnalytics(campaignId);
      setReport(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    try {
      setAnalyzing(true);
      const data = await api.analyzeCampaign(campaignId);
      setReport(data);
    } catch (error) {
      console.error(error);
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) return <div className="p-8">Loading Analytics...</div>;
  if (!report) return <div className="p-8">Failed to load analytics.</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Campaign Analytics</h1>
          <p className="text-muted-foreground">Performance metrics, diagnostics, and AI recommendations</p>
        </div>
        <Button onClick={handleAnalyze} disabled={analyzing}>
          {analyzing ? "AI is Analyzing..." : "Run AI Analysis"}
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Spend</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${report.performance.spend.toFixed(2)}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Clicks</CardTitle>
            <MousePointerClick className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{report.performance.clicks}</div>
            <p className="text-xs text-muted-foreground">CTR: {report.performance.ctr.toFixed(2)}%</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversions</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{report.performance.conversions}</div>
            <p className="text-xs text-muted-foreground">CPA: ${report.performance.cpa.toFixed(2)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">ROAS</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{report.performance.roas.toFixed(2)}x</div>
            <p className="text-xs text-muted-foreground">Revenue: ${report.performance.revenue.toFixed(2)}</p>
          </CardContent>
        </Card>
      </div>

      {report.diagnostics.length > 0 && (
        <Card className="border-orange-200 bg-orange-50">
          <CardHeader>
            <CardTitle className="flex items-center text-orange-800">
              <AlertTriangle className="mr-2 h-5 w-5" />
              Diagnostics Warnings
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="list-disc pl-5 space-y-1 text-orange-800">
              {report.diagnostics.map((diag, i) => (
                <li key={i}>{diag.message}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>AI Insights</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {report.insights.length === 0 ? (
              <p className="text-sm text-muted-foreground">Click "Run AI Analysis" to generate insights.</p>
            ) : (
              report.insights.map((insight, i) => (
                <div key={i} className="rounded-lg border p-3">
                  <div className="font-semibold">{insight.category}</div>
                  <div className="text-sm mt-1">{insight.message}</div>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Optimization Recommendations</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {report.recommendations.length === 0 ? (
              <p className="text-sm text-muted-foreground">No recommendations pending.</p>
            ) : (
              report.recommendations.map((rec, i) => (
                <div key={i} className="rounded-lg border p-3">
                  <div className="font-semibold text-blue-600">{rec.type}</div>
                  <div className="text-sm mt-1">{rec.description}</div>
                  <div className="mt-2 flex gap-2">
                    <Button size="sm" variant="outline" className="text-green-600">Approve</Button>
                    <Button size="sm" variant="outline" className="text-red-600">Reject</Button>
                  </div>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
